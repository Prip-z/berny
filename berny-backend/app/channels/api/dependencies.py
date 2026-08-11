from typing import Annotated

from app.channels.application.CRUDUseCase import (
    CreateChannelUseCase,
    CreateDirectChannelUseCase,
    DeleteChannelUseCase,
    GetChannelByIdUseCase,
    GetChannelMembersUseCase,
    GetDirectChannelBetweenUsers,
    RemoveChannelMemberSelfUseCase,
    RemoveChannelMemberUseCase,
    UpdateChannelMemberUseCase,
    UpdateChannelUseCase,
)
from app.channels.application.GetUserChannelsUseCase import GetUserChannelsUseCase
from app.channels.application.SearchChannelUseCase import SearchChannelUseCase
from app.channels.infrastructure.repositories.ChannelRepository import ChannelRepository
from app.shared.infrastructure.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_channel_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ChannelRepository:
    return ChannelRepository(session)


def get_create_channel_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> CreateChannelUseCase:
    return CreateChannelUseCase(repo)


def get_channel_by_id_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> GetChannelByIdUseCase:
    return GetChannelByIdUseCase(repo)


def get_update_channel_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> UpdateChannelUseCase:
    return UpdateChannelUseCase(repo)


def get_delete_channel_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> DeleteChannelUseCase:
    return DeleteChannelUseCase(repo)


def get_add_member_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> UpdateChannelMemberUseCase:
    return UpdateChannelMemberUseCase(repo)


def get_remove_member_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> RemoveChannelMemberUseCase:
    return RemoveChannelMemberUseCase(repo)


def get_get_members_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> GetChannelMembersUseCase:
    return GetChannelMembersUseCase(repo)


def get_search_channel_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> SearchChannelUseCase:
    return SearchChannelUseCase(repo)


def get_create_direct_channel_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> CreateDirectChannelUseCase:
    return CreateDirectChannelUseCase(repo)


def get_user_channels_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> GetUserChannelsUseCase:
    return GetUserChannelsUseCase(repo)


def get_direct_channel_between_users_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> GetDirectChannelBetweenUsers:
    return GetDirectChannelBetweenUsers(repo)


def get_update_channel_member_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> UpdateChannelMemberUseCase:
    return UpdateChannelMemberUseCase(repo)

def get_remove_member_self_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> RemoveChannelMemberSelfUseCase:
    return RemoveChannelMemberSelfUseCase(repo)
