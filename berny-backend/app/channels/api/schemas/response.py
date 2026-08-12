from datetime import datetime
from uuid import UUID

from app.channels.domain.entity.Channel import ChannelType
from app.channels.domain.entity.ChannelMembers import UserRole
from pydantic import BaseModel


class UserChannelResponse(BaseModel):
    channel_id: UUID
    type: ChannelType
    name: str | None
    target_user_id: UUID | None
    last_message_text: str | None = None
    last_message_at: datetime | None = None


class CreateChannelRequest(BaseModel):
    name: str | None = None
    channel_type: ChannelType


class AddMemberRequest(BaseModel):
    added_user_id: UUID
    role: UserRole
