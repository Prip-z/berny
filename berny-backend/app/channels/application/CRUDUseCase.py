from uuid import UUID

from app.channels.domain.entity.Channel import Channel, ChannelType, ChannelUpdateData
from app.channels.domain.entity.ChannelMembers import ChannelMembers, UserRole
from app.channels.domain.interface.IChannelRepository import IChannelRepository


class CreateChannelUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(
        self, name: str | None, channel_type: ChannelType, creator_id: UUID
    ) -> Channel:
        channel = Channel(name=name, type=channel_type)
        created_channel = await self._channel_repo.create_channel(channel)

        await self._channel_repo.add_member(
            channel_id=created_channel.channel_id,
            user_id=creator_id,
            role=UserRole.ADMIN,
        )
        return created_channel


class GetChannelByIdUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(self, channel_id: UUID) -> Channel:
        return await self._channel_repo.get_with_id(channel_id)


class UpdateChannelUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(
        self, channel_id: UUID, changes: ChannelUpdateData
    ) -> Channel | None:
        return await self._channel_repo.update_channel(channel_id, changes)


class DeleteChannelUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(self, channel_id: UUID) -> bool:
        return await self._channel_repo.delete_channel(channel_id)


class AddChannelMemberUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(
        self, channel_id: UUID, user_id: UUID, role: UserRole = UserRole.READER
    ) -> ChannelMembers:
        return await self._channel_repo.add_member(channel_id, user_id, role)


class RemoveChannelMemberUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(self, channel_id: UUID, user_id: UUID) -> bool:
        return await self._channel_repo.remove_member(channel_id, user_id)


class GetChannelMembersUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(self, channel_id: UUID) -> list[ChannelMembers]:
        return await self._channel_repo.get_members(channel_id)
