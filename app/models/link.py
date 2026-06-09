from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    icon = Column(String, default="link", nullable=False)
    clicks = Column(Integer, default=0, nullable=False)
    order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="links")
