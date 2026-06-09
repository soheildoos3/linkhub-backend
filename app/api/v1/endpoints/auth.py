from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from sqlalchemy.orm import Session
from app.core.security import verify_password
from app.core.auth import (
    set_auth_cookies,
    clear_auth_cookies,
    refresh_access_token,
    create_auth_tokens,
)
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=UserResponse)
def login(user_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token, refresh_token = create_auth_tokens(user.username)
    set_auth_cookies(response, access_token, refresh_token)

    return user


@router.post("/logout")
def logout(response: Response):
    clear_auth_cookies(response)
    return {"message": "Logout successful"}


@router.post("/refresh")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    new_access_token = refresh_access_token(request, response, db)

    return {"message": "Token refreshed successfully"}
