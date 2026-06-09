from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "LinkHub API"
    PROJECT_DESCRIPTION: str = """
    ## LinkHub Platform API
    
    LinkHub is a platform for users to share and manage their links.
    
    ### Features:
    - 🔐 User authentication (register, login, logout)
    - 📝 Create, update, delete links
    - 👤 User profile management
    - 🌐 Public user pages (like Linktree)
    - 📊 Link click statistics
    
    ### Authentication:
    Uses JWT tokens stored in HTTP-only cookies.
    """
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str

    DATABASE_URL: str

    ALGORITHM: str
    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    COOKIE_NAME: str = "access_token"
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: str = "lax"

    CORS_ORIGINS: str
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def COOKIE_SECURE(self) -> bool:
        """Secure cookie only in production"""
        return self.ENVIRONMENT == "production"


settings = Settings()
