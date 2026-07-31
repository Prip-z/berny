from typing import Annotated
from uuid import UUID

from app.channels.api.dependencies import (
    get_add_member_use_case,
    get_channel_by_id_use_case,
    get_create_channel_use_case,
    get_delete_channel_use_case,
    get_get_members_use_case,
    get_remove_member_use_case,
    get_update_channel_use_case,
)
from app.channels.application.CRUDUseCase import (
    AddChannelMemberUseCase,
    CreateChannelUseCase,
    DeleteChannelUseCase,
    GetChannelByIdUseCase,
    GetChannelMembersUseCase,
    RemoveChannelMemberUseCase,
    UpdateChannelUseCase,
)
from app.channels.domain.entity.Channel import Channel, ChannelType, ChannelUpdateData
from app.channels.domain.entity.ChannelMembers import ChannelMembers, UserRole
from fastapi import APIRouter, Depends, status

channel_router = APIRouter(prefix="/channels", tags=["Channels"])


@channel_router.post("/", response_model=Channel, status_code=status.HTTP_201_CREATED)
async def create_channel(
    name: str | None,
    channel_type: ChannelType,
    creator_id: UUID,
    use_case: Annotated[CreateChannelUseCase, Depends(get_create_channel_use_case)],
):
    return await use_case(name=name, channel_type=channel_type, creator_id=creator_id)


@channel_router.get("/{channel_id}", response_model=Channel)
async def get_channel_by_id(
    channel_id: UUID,
    use_case: Annotated[GetChannelByIdUseCase, Depends(get_channel_by_id_use_case)],
):
    return await use_case(channel_id=channel_id)


@channel_router.patch("/{channel_id}", response_model=Channel | None)
async def update_channel(
    channel_id: UUID,
    changes: ChannelUpdateData,
    use_case: Annotated[UpdateChannelUseCase, Depends(get_update_channel_use_case)],
):
    return await use_case(channel_id=channel_id, changes=changes)


@channel_router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    channel_id: UUID,
    use_case: Annotated[DeleteChannelUseCase, Depends(get_delete_channel_use_case)],
):
    await use_case(channel_id=channel_id)


@channel_router.post("/{channel_id}/members", response_model=ChannelMembers)
async def add_member(
    channel_id: UUID,
    user_id: UUID,
    role: UserRole,
    use_case: Annotated[AddChannelMemberUseCase, Depends(get_add_member_use_case)],
):
    return await use_case(channel_id=channel_id, user_id=user_id, role=role)


@channel_router.delete(
    "/{channel_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def remove_member(
    channel_id: UUID,
    user_id: UUID,
    use_case: Annotated[
        RemoveChannelMemberUseCase, Depends(get_remove_member_use_case)
    ],
):
    await use_case(channel_id=channel_id, user_id=user_id)


@channel_router.get("/{channel_id}/members", response_model=list[ChannelMembers])
async def get_members(
    channel_id: UUID,
    use_case: Annotated[GetChannelMembersUseCase, Depends(get_get_members_use_case)],
):
    return await use_case(channel_id=channel_id)
