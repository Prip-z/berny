from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.infrastructure.database import get_db
from app.channels.infrastructure.repositories.ChannelRepository import ChannelRepository
from app.channels.application.CRUDUseCase import (
    AddChannelMemberUseCase,
    CreateChannelUseCase,
    DeleteChannelUseCase,
    GetChannelByIdUseCase,
    GetChannelMembersUseCase,
    RemoveChannelMemberUseCase,
    UpdateChannelUseCase,
)


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
) -> AddChannelMemberUseCase:
    return AddChannelMemberUseCase(repo)


def get_remove_member_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> RemoveChannelMemberUseCase:
    return RemoveChannelMemberUseCase(repo)


def get_get_members_use_case(
    repo: Annotated[ChannelRepository, Depends(get_channel_repository)],
) -> GetChannelMembersUseCase:
    return GetChannelMembersUseCase(repo)