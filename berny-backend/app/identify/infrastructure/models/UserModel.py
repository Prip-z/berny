import uuid
from datetime import datetime

from app.identify.infrastructure.database import Base
from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255))
    last_seen: Mapped[datetime | None] = mapped_column(default=None)
