import uuid
from datetime import datetime

from app.channels.domain.entity.Channel import ChannelType
from app.shared.infrastructure.database import Base
from sqlalchemy import UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column


class Channel(Base):
    __tablename__ = "channel"

    channel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[ChannelType] = mapped_column(Enum(ChannelType))
    last_message_text: Mapped[str] = mapped_column(nullable=True)
    last_message_at: Mapped[datetime] = mapped_column(nullable=True)
