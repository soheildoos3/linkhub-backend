from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User


def check_existing_user(db: Session, email: str, username: str) -> None:
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    existing_username = db.query(User).filter(User.username == username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )


def check_existing_email(db: Session, email: str, exclude_user_id: int = None) -> None:
    query = db.query(User).filter(User.email == email)
    if exclude_user_id:
        query = query.filter(User.id != exclude_user_id)

    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used"
        )


def check_existing_username(
    db: Session, username: str, exclude_user_id: int = None
) -> None:
    query = db.query(User).filter(User.username == username)
    if exclude_user_id:
        query = query.filter(User.id != exclude_user_id)

    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )
