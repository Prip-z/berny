from datetime import datetime, timezone
from uuid import UUID

from app.messaging.domain.interfaces.IChannelAccessValidator import (
    IChannelAccessValidator,
)
from app.messaging.domain.Message import Message
from app.messaging.infrastructure.repositories import ScyllaMessageRepository
from app.shared.exception import AccessDenied


class GetChannelMessagesUseCase:
    def __init__(
        self,
        repo: ScyllaMessageRepository,
        access_validator: IChannelAccessValidator,
    ):
        self.repo = repo
        self.access_validator = access_validator

    async def __call__(
        self,
        current_user_id: UUID,
        channel_id: UUID,
        limit: int = 50,
        before_id: int | None = None,
    ) -> list[Message]:
        has_access = self.access_validator.can_send_message(
            user_id=current_user_id, channel_id=channel_id
        )
        if not has_access:
            raise AccessDenied

        current_bucket = datetime.now(timezone.utc).strftime("%Y-%m")
        return await self.repo.get_messages_by_channel(
            channel_id=channel_id,
            time_bucket=current_bucket,
            limit=limit,
            before_id=before_id,
        )
