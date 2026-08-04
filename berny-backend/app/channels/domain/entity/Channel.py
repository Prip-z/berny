from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class ChannelType(Enum):
    DIRECT = "direct"
    GROUP = "group"
    PUBLIC = "public"


class Channel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    channel_id: UUID = Field(default_factory=uuid4)
    name: str | None = None
    type: ChannelType


class ChannelUpdateData(BaseModel):
    name: str | None = None
    type: ChannelType | None
    