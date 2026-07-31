from app.messaging.infrastructure.brokers import MessageBroker
from app.shared.lib.snowflake_id import get_snowflake_id
from app.messaging.domain.Message import Message
from app.messaging.infrastructure.repositories import ScyllaMessageRepository

class SendMessagingUseCase:
    def __init__(self, repo: ScyllaMessageRepository, broker: MessageBroker):
        self.repo = repo
        self.broker = broker

    async def __call__(self, sender_id: int, channel_id: int, text: str) -> Message:
        message_id = get_snowflake_id()
        
        message = Message(
            message_id=message_id,
            channel_id=channel_id,
            sender_id=sender_id,
            text=text
        )

        await self.repo.save(message)

        payload = message.model_dump(mode="json")  
        await self.broker.publishMessage("chat_events", payload)

        return message

    