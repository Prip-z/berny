from uuid import UUID

from app.messaging.domain.interfaces.IChannelAccessValidator import (
    IChannelAccessValidator,
)
from app.messaging.domain.Message import Message
from app.messaging.infrastructure.brokers import MessageBroker
from app.messaging.infrastructure.repositories import ScyllaMessageRepository
from app.shared.exception import AccessDenied
from app.shared.lib.snowflake_id import get_snowflake_id


class SendMessagingUseCase:
    def __init__(
        self,
        repo: ScyllaMessageRepository,
        broker: MessageBroker,
        access_validator: IChannelAccessValidator,
    ):
        self.repo = repo
        self.broker = broker
        self.access_validator = access_validator

    async def __call__(self, sender_id: UUID, channel_id: UUID, text: str) -> Message:
        has_access = self.access_validator.can_send_message(user_id=sender_id, channel_id=channel_id)
        if not has_access:
            raise AccessDenied
        message_id = get_snowflake_id()

        message = Message(
            message_id=message_id, 
            channel_id=channel_id, 
            sender_id=sender_id, 
            text=text
        )

        await self.repo.save(message)

        member_ids = await self.access_validator.get_channel_members_ids(channel_id)
        payload = {
            "target_user_ids": [str(uid) for uid in member_ids],
            "event_type": "NEW_MESSAGE",
            "payload": message.model_dump(mode="json")
        }
        await self.broker.publishMessage("chat_events", payload)

        return message
