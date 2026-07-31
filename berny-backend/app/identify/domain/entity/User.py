from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class UserAuthProvider(str, Enum):
    GOOGLE = "google"
    LOCAL = "local"


class User(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    username: str
    email: str
    password_hash: str | None
    last_seen: datetime | None = Field(default=None)
    # auth_provider: UserAuthProvider | None
    # provider_id: str | None
    model_config = ConfigDict(from_attributes=True)


class UserUpdateData(BaseModel):
    username: str | None = None
    email: str | None = None
    password_hash: str | None = None
    last_seen: datetime | None = None
