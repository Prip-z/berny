from abc import ABC, abstractmethod
from uuid import UUID

from app.channels.domain.dto.UserChannel import UserChannel
from app.channels.domain.entity.Channel import Channel, ChannelUpdateData
from app.channels.domain.entity.ChannelMembers import ChannelMembers, UserRole
from app.channels.domain.entity.SearchResultItem import SearchResultItem
from sqlalchemy.ext.asyncio import AsyncSession


class IChannelRepository(ABC):
    def __init__(self, _session: AsyncSession):
        pass

    @abstractmethod
    async def get_user_role(self, channel_id: UUID, user_id: UUID) -> UserRole:
        pass

    @abstractmethod
    async def get_members(self, channel_id: UUID) -> list[ChannelMembers]:
        pass

    @abstractmethod
    async def remove_member(self, channel_id: UUID, user_id: UUID) -> bool:
        pass

    @abstractmethod
    async def add_member(
        self, channel_id: UUID, user_id: UUID, role: UserRole
    ) -> ChannelMembers:
        pass

    @abstractmethod
    async def search_channel(
        self, search_query: str, current_user_id: UUID
    ) -> list[SearchResultItem]:
        pass

    @abstractmethod
    async def get_with_id(self, channel_id: UUID) -> Channel:
        pass

    @abstractmethod
    async def create_channel(self, channel: Channel) -> Channel:
        pass

    @abstractmethod
    async def update_channel(
        self, channel_id: UUID, changes: ChannelUpdateData
    ) -> Channel | None:
        pass

    @abstractmethod
    async def delete_channel(self, channel_id: UUID) -> bool:
        pass

    @abstractmethod
    async def get_direct_channel_between_users(
        self, user1_id: UUID, user2_id: UUID
    ) -> Channel | None:
        pass

    @abstractmethod
    async def get_user_channels(self, current_user_id: UUID) -> list[UserChannel]:
        pass
