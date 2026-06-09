from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, List
from datetime import datetime
from app.schemas.validators import Platform, normalize_url_by_platform


class LinkBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Title of the link",
        example="My Instagram",
    )
    url: str = Field(
        ...,
        description="Full URL address (http://, https://, tel:, or mailto:)",
        example="https://instagram.com/username",
    )
    icon: Platform = Field(
        default=Platform.LINK,
        description="Platform icon to display",
        example=Platform.INSTAGRAM,
    )
    order: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_url_by_platform(self):
        if self.url:
            self.url = normalize_url_by_platform(self.url, self.icon)
        return self


class LinkCreate(LinkBase):
    pass


class LinkUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Title of the link",
        example="My Updated Instagram",
    )
    url: Optional[str] = Field(
        None,
        description="Full URL address",
        example="https://instagram.com/new_username",
    )
    icon: Optional[Platform] = Field(
        None, description="Platform icon", example=Platform.INSTAGRAM
    )
    order: Optional[int] = Field(None, ge=0)

    @model_validator(mode="after")
    def validate_url_by_platform(self):
        if self.url and self.icon:
            self.url = normalize_url_by_platform(self.url, self.icon)
        return self


class LinkResponse(LinkBase):
    id: int
    user_id: int
    clicks: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class LinkListResponse(BaseModel):
    namelink: str
    username: Optional[str] = None
    items: List[LinkResponse]


class LinksListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[LinkListResponse]
