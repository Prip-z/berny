from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field, computed_field, field_serializer


class Message(BaseModel):
    message_id: int
    channel_id: UUID
    sender_id: UUID
    text: str | None = Field(min_length=1, max_length=3000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # attachments: list[Attachment] = Field(default_factory=list)

    @computed_field
    def time_bucket(self) -> str:
        return self.created_at.strftime("%Y-%m")

    @field_serializer("message_id")
    def serialize_message_id(self, value: int) -> str:
        return str(value)
