from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    model_validator,
)
from datetime import datetime
from typing import Optional
from app.schemas.validators import normalize_username


class UserBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="Full name of the user",
        example="Ali Rezaei",
    )
    namelink: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="Display name on public page",
        example="Ali R",
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username for login and profile URL (letters, numbers, hyphen)",
        example="ali-rezaei",
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address",
        example="ali@example.com",
    )

    @model_validator(mode="after")
    def normalize_username(self) -> "UserBase":
        if self.username:
            self.username = normalize_username(self.username)
        return self


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Password must be at least 6 characters long",
        example="123456",
    )
    confirm_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Repeat the password to confirm",
        example="123456",
    )

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserCreate":
        if self.password and self.confirm_password:
            if self.password != self.confirm_password:
                raise ValueError("The password and its repetition do not match.")
        return self


class UserLogin(BaseModel):
    email: EmailStr = Field(
        ..., description="Your registered email address", example="ali@example.com"
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Your account password",
        example="123456",
    )


class UserUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="Full name of the user",
        example="Ali Rezaei",
    )
    namelink: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="Display name on public page",
        example="Ali R",
    )
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="Unique username (letters, numbers, underscore, hyphen)",
        example="ali-rezaei",
    )
    email: Optional[EmailStr] = Field(
        None, description="Valid email address", example="newemail@example.com"
    )

    @model_validator(mode="after")
    def normalize_username(self) -> "UserBase":
        if self.username:
            self.username = normalize_username(self.username)
        return self


class PasswordChange(BaseModel):
    old_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Your current password",
        example="123456",
    )
    new_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="New password (must be different from old password)",
        example="NewP@ss456",
    )
    confirm_new_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Repeat the new password",
        example="NewP@ss456",
    )

    @model_validator(mode="after")
    def validate_passwords(self) -> "PasswordChange":
        """Validate all password-related rules"""
        if self.old_password and self.new_password:
            if self.new_password == self.old_password:
                raise ValueError(
                    "The new password must not be the same as the old password."
                )
        if self.new_password and self.confirm_new_password:
            if self.new_password != self.confirm_new_password:
                raise ValueError("The new password and its repetition do not match.")
        return self


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
