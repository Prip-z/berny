from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class UserRole(Enum):
    ADMIN = "admin"
    READER = "reader"
    EDITOR = "editor"
    DIRECT_PARTICIPANT = "direct_paricipant"

class ChannelMembers(BaseModel):
    channel_id: UUID
    user_id: UUID
    role: UserRole | None
