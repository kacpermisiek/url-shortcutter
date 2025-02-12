import uuid

from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from url_shortcutter.db import Base


class Url(Base):
    __tablename__ = "url"
    __table_args__ = (UniqueConstraint("url"),)  # This could be also (UniqueConstraint("url", "created_by_ip"),)

    id = Column(UUID, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    url = Column(String, index=True)
    short_suffix = Column(String, index=True)
    visits = Column(Integer, default=0)
    created_by_ip = Column(String, nullable=True)
    created_by_user_agent = Column(String, nullable=True)
