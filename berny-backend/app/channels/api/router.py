from typing import Annotated
from uuid import UUID

from app.channels.api.dependencies import (
    get_add_member_use_case,
    get_channel_by_id_use_case,
    get_create_channel_use_case,
    get_create_direct_channel_use_case,
    get_delete_channel_use_case,
    get_direct_channel_between_users_use_case,
    get_get_members_use_case,
    get_remove_member_self_use_case,
    get_remove_member_use_case,
    get_search_channel_use_case,
    get_update_channel_member_use_case,
    get_update_channel_use_case,
    get_user_channels_use_case,
)
from app.channels.api.schemas.response import UserChannelResponse
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
from app.channels.domain.entity.Channel import Channel, ChannelType, ChannelUpdateData
from app.channels.domain.entity.ChannelMembers import ChannelMembers, UserRole
from app.channels.domain.entity.SearchResultItem import SearchResultItem
from app.shared.api.dependencies import get_current_user_payload
from fastapi import APIRouter, Depends, status

channel_router = APIRouter(prefix="/channels", tags=["Channels"])


@channel_router.get("/search", response_model=list[SearchResultItem])
async def search_channel(
    use_case: Annotated[SearchChannelUseCase, Depends(get_search_channel_use_case)],
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
    search_query: str = "",
):
    return await use_case(current_user_id, search_query)


@channel_router.post("/", response_model=Channel, status_code=status.HTTP_201_CREATED)
async def create_channel(
    name: str | None,
    channel_type: ChannelType,
    use_case: Annotated[CreateChannelUseCase, Depends(get_create_channel_use_case)],
    creator_id: Annotated[UUID, Depends(get_current_user_payload)],
):
    return await use_case(name=name, channel_type=channel_type, creator_id=creator_id)


@channel_router.post(
    "/direct/{target_user_id}",
    response_model=Channel,
    status_code=status.HTTP_201_CREATED,
)
async def create_direct_channel(
    target_user_id: UUID,
    use_case: Annotated[
        CreateDirectChannelUseCase, Depends(get_create_direct_channel_use_case)
    ],
    creator_id: Annotated[UUID, Depends(get_current_user_payload)],
):
    return await use_case(current_user_id=creator_id, target_user_id=target_user_id)


@channel_router.get("/{channel_id}", response_model=Channel)
async def get_channel_by_id(
    channel_id: UUID,
    use_case: Annotated[GetChannelByIdUseCase, Depends(get_channel_by_id_use_case)],
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
):
    return await use_case(channel_id=channel_id)


@channel_router.patch("/{channel_id}", response_model=Channel | None)
async def update_channel(
    channel_id: UUID,
    changes: ChannelUpdateData,
    use_case: Annotated[UpdateChannelUseCase, Depends(get_update_channel_use_case)],
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
):
    return await use_case(
        channel_id=channel_id, changes=changes, user_id=current_user_id
    )


@channel_router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    channel_id: UUID,
    use_case: Annotated[DeleteChannelUseCase, Depends(get_delete_channel_use_case)],
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
):
    await use_case(channel_id=channel_id, current_user_id=current_user_id)


@channel_router.post("/{channel_id}/members", response_model=ChannelMembers)
async def add_member(
    channel_id: UUID,
    added_user_id: UUID,
    role: UserRole,
    use_case: Annotated[UpdateChannelMemberUseCase, Depends(get_add_member_use_case)],
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
):
    return await use_case(
        channel_id=channel_id,
        added_user_id=added_user_id,
        role=role,
        current_user_id=current_user_id,
    )


@channel_router.delete(
    "/{channel_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def remove_member(
    channel_id: UUID,
    user_id: UUID,
    use_case: Annotated[
        RemoveChannelMemberUseCase, Depends(get_remove_member_use_case)
    ],
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
):
    await use_case(
        channel_id=channel_id, user_id=user_id, current_user_id=current_user_id
    )


@channel_router.get("/{channel_id}/members", response_model=list[ChannelMembers])
async def get_members(
    channel_id: UUID,
    use_case: Annotated[GetChannelMembersUseCase, Depends(get_get_members_use_case)],
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
):
    return await use_case(channel_id=channel_id)


@channel_router.get("/", response_model=list[UserChannelResponse])
async def get_my_channels(
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
    use_case: Annotated[GetUserChannelsUseCase, Depends(get_user_channels_use_case)],
):

    return await use_case(current_user_id=current_user_id)


@channel_router.get(
    "/direct/{target_user_search_query}", response_model=list[UserChannelResponse]
)
async def get_direct_channel_between_user(
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
    use_case: Annotated[
        GetDirectChannelBetweenUsers, Depends(get_direct_channel_between_users_use_case)
    ],
    target_user_search_query: UUID,
):

    return await use_case(
        current_user_id=current_user_id, target_user_id=target_user_search_query
    )


@channel_router.patch("/update/{channel_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_channel_member(
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
    use_case: Annotated[
        UpdateChannelMemberUseCase, Depends(get_update_channel_member_use_case)
    ],
    channel_id: UUID,
    target_user_id: UUID,
    role: UserRole,
):
    return await use_case(
        channel_id=channel_id,
        added_user_id=target_user_id,
        current_user_id=current_user_id,
        role=role,
    )

@channel_router.delete(
    "/{channel_id}/members/", status_code=status.HTTP_204_NO_CONTENT
)
async def remove_member_self(
    channel_id: UUID,
    use_case: Annotated[
        RemoveChannelMemberSelfUseCase, Depends(get_remove_member_self_use_case)
    ],
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
):
    await use_case(
        channel_id=channel_id, current_user_id=current_user_id
    )