from abc import ABC, abstractmethod
from uuid import UUID


class IChannelAccessValidator(ABC):
    @abstractmethod
    async def can_send_message(self, user_id: UUID, channel_id: UUID) -> bool:
        pass

    @abstractmethod
    async def get_channel_members_ids(self, channel_id: UUID) -> list[UUID]:
        pass
