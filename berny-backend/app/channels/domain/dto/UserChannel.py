from datetime import datetime
from uuid import UUID

from app.channels.domain.entity.Channel import ChannelType
from pydantic import BaseModel


class UserChannel(BaseModel):
    channel_id: UUID
    type: ChannelType
    name: str | None
    target_user_id: UUID | None = None
    last_message_text: str | None = None
    last_message_at: datetime | None = None
