from uuid import UUID

from app.channels.domain.entity.Channel import Channel, ChannelType, ChannelUpdateData
from app.channels.domain.entity.ChannelMembers import ChannelMembers, UserRole
from app.channels.domain.exception import InvalidChannelType
from app.channels.domain.interface.IChannelRepository import IChannelRepository
from app.shared.exception import AccessDenied


class CreateChannelUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(
        self,
        name: str | None,
        channel_type: ChannelType,
        creator_id: UUID,
    ) -> Channel:

        channel = Channel(name=name, type=channel_type)
        created_channel = await self._channel_repo.create_channel(channel)
        if channel_type == "direct":
            raise InvalidChannelType
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
        self, channel_id: UUID, changes: ChannelUpdateData, user_id: UUID
    ) -> Channel | None:
        role = await self._channel_repo.get_user_role(channel_id, user_id)
        if role == UserRole.READER:
            raise AccessDenied
        return await self._channel_repo.update_channel(channel_id, changes)


class DeleteChannelUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(self, channel_id: UUID, current_user_id: UUID) -> bool:
        role = await self._channel_repo.get_user_role(channel_id, current_user_id)
        if role == UserRole.READER:
            raise AccessDenied
        return await self._channel_repo.delete_channel(channel_id)


class AddChannelMemberUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(
        self,
        channel_id: UUID,
        added_user_id: UUID,
        current_user_id: UUID,
        role: UserRole = UserRole.READER,
    ) -> ChannelMembers:
        role = await self._channel_repo.get_user_role(channel_id, current_user_id)
        if role == UserRole.READER:
            raise AccessDenied
        return await self._channel_repo.add_member(channel_id, added_user_id, role)


class RemoveChannelMemberUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(
        self, channel_id: UUID, user_id: UUID, current_user_id: UUID
    ) -> bool:
        role = await self._channel_repo.get_user_role(channel_id, current_user_id)
        if role == UserRole.READER:
            raise AccessDenied
        return await self._channel_repo.remove_member(channel_id, user_id)


class GetChannelMembersUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(self, channel_id: UUID) -> list[ChannelMembers]:
        return await self._channel_repo.get_members(channel_id)


class GetMemberChannelRole:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(self, channel_id: UUID, user_id: UUID):
        return await self._channel_repo.get_user_role(channel_id, user_id)

class CreateDirectChannelUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(
        self, current_user_id: UUID, target_user_id: UUID
    ) -> Channel:
        if current_user_id == target_user_id:
            raise ValueError("Cannot create a direct chat with yourself")

        existing_channel = await self._channel_repo.get_direct_channel_between_users(
            current_user_id, target_user_id
        )
        if existing_channel:
            return existing_channel

        new_channel = Channel(name=None, type=ChannelType.DIRECT)
        created_channel = await self._channel_repo.create_channel(new_channel)

        await self._channel_repo.add_member(
            channel_id=created_channel.channel_id,
            user_id=current_user_id,
            role=UserRole.DIRECT_PARTICIPANT,
        )
        await self._channel_repo.add_member(
            channel_id=created_channel.channel_id,
            user_id=target_user_id,
            role=UserRole.DIRECT_PARTICIPANT,
        )

        return created_channel