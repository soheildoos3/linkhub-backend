from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.link import Link
from app.schemas.link import (
    LinkCreate,
    LinkResponse,
    LinkUpdate,
    LinkListResponse,
    LinksListResponse,
)

router = APIRouter(prefix="/links", tags=["Links"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_link(
    link_data: LinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    link_count = db.query(Link).filter(Link.user_id == current_user.id).count()
    if link_count >= 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum number of links (50) reached",
        )

    new_link = Link(**link_data.model_dump(), user_id=current_user.id)
    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    return new_link


@router.get("/", response_model=LinksListResponse)
def get_links(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(User).filter(User.links.any())
    if search and search.strip():
        search_term = f"%{search.strip()}%"
        query = query.filter(
            (User.username.ilike(search_term)) | (User.namelink.ilike(search_term))
        )

    total = query.count()
    users = query.offset(skip).limit(limit).all()

    result = []
    for user in users:
        sorted_links = sorted(user.links, key=lambda x: x.order)

        items = []
        for link in sorted_links:
            link_response = LinkResponse(
                id=link.id,
                title=link.title,
                url=link.url,
                icon=link.icon,
                order=link.order,
                user_id=link.user_id,
                clicks=link.clicks,
                created_at=link.created_at,
                updated_at=link.updated_at,
            )
            items.append(link_response)

        result.append(
            LinkListResponse(
                namelink=user.namelink if user.namelink else user.username,
                username=user.username,
                items=items,
            )
        )

    return LinksListResponse(items=result, total=total, skip=skip, limit=limit)


@router.get("/{username}/{link_id}")
def redirect_to_link(
    username: str,
    link_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    link = db.query(Link).filter(Link.id == link_id, Link.user_id == user.id).first()

    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
        )

    link.clicks += 1
    db.commit()

    return RedirectResponse(url=link.url, status_code=status.HTTP_302_FOUND)


@router.get("/{username}", response_model=LinkListResponse)
def get_link(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    links = db.query(Link).filter(Link.user_id == user.id).order_by(Link.order).all()

    return LinkListResponse(
        namelink=user.namelink or user.username, username=user.username, items=links
    )


@router.patch("/{link_id}", response_model=LinkResponse)  # PUT -> PATCH
def update_link(
    link_id: int,
    link_data: LinkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    link = (
        db.query(Link)
        .filter(Link.id == link_id, Link.user_id == current_user.id)
        .first()
    )
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found or you don't have permission to edit it.",
        )

    update_data = link_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(link, field, value)

    db.commit()
    db.refresh(link)

    return link


@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(
    link_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    link = (
        db.query(Link)
        .filter(Link.id == link_id, Link.user_id == current_user.id)
        .first()
    )
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found or you don't have permission to edit it.",
        )

    db.delete(link)
    db.commit()

    return None


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_links(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    deleted_count = db.query(Link).filter(Link.user_id == current_user.id).delete()

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No links found to delete.",
        )

    db.commit()
    return None
