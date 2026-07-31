from datetime import datetime, timezone
from pydantic import BaseModel, Field, computed_field
# from uuid import UUID   

class Message(BaseModel):
    message_id: int
    channel_id: int
    sender_id: int
    text: str | None = Field(min_length=1, max_length=3000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # attachments: list[Attachment] = Field(default_factory=list)

    @computed_field
    @property
    def time_bucket(self) -> str:
        return self.created_at.strftime("%Y-%m")
