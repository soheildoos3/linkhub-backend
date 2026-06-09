from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password

from app.core.auth import (
    set_auth_cookies,
    get_current_user,
    create_auth_tokens,
)
from app.core.user_utils import (
    check_existing_user,
    check_existing_username,
    check_existing_email,
)
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    PasswordChange,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user_data: UserCreate, response: Response, db: Session = Depends(get_db)):
    check_existing_user(db, user_data.email, user_data.username)

    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        name=user_data.name,
        namelink=user_data.namelink,
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token, refresh_token = create_auth_tokens(new_user.username)
    set_auth_cookies(response, access_token, refresh_token)

    return new_user


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_user(
    user_data: UserUpdate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    username_changed = False

    if user_data.username and user_data.username != current_user.username:
        check_existing_username(db, user_data.username, current_user.id)
        current_user.username = user_data.username
        username_changed = True

    if user_data.email and user_data.email != current_user.email:
        check_existing_email(db, user_data.email, current_user.id)
        current_user.email = user_data.email

    if user_data.name is not None:
        current_user.name = user_data.name
    if user_data.namelink is not None:
        current_user.namelink = user_data.namelink

    db.commit()
    db.refresh(current_user)

    if username_changed and response:
        from app.core.security import create_access_token, create_refresh_token
        from app.core.auth import set_auth_cookies

        new_access_token = create_access_token(data={"sub": current_user.username})
        new_refresh_token = create_refresh_token(data={"sub": current_user.username})
        set_auth_cookies(response, new_access_token, new_refresh_token)

    return current_user


@router.put("/change-password", response_model=UserResponse)
def change_password(
    user_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(user_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Old password is incorrect"
        )

    current_user.password_hash = get_password_hash(user_data.new_password)

    db.commit()
    db.refresh(current_user)

    return current_user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db.delete(current_user)
    db.commit()

    return None
