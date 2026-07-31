import uuid

from app.channels.domain.entity.ChannelMembers import UserRole
from app.shared.infrastructure.database import Base
from sqlalchemy import UUID, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class ChannelMembersORM(Base):
    __tablename__ = "channel_members"

    channel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("channel.channel_id", ondelete="CASCADE"), 
        primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), 
        default=UserRole.READER, 
        nullable=False
    )