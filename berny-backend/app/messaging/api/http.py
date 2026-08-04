from fastapi import APIRouter

message_router = APIRouter(prefix="message")

from typing import Annotated
from uuid import UUID

from app.messaging.api.dependencies import get_channel_messages_use_case
from app.messaging.application.GetChannelMessagesUseCase import (
    GetChannelMessagesUseCase,
)
from app.messaging.domain.Message import Message
from app.shared.api.dependencies import get_current_user_payload
from fastapi import APIRouter, Depends, Query

messaging_router = APIRouter(prefix="/messaging", tags=["Messaging"])


@messaging_router.get("/channels/{channel_id}/messages", response_model=list[Message])
async def get_channel_messages(
    channel_id: UUID,
    current_user_id: Annotated[UUID, Depends(get_current_user_payload)],
    use_case: Annotated[
        GetChannelMessagesUseCase, Depends(get_channel_messages_use_case)
    ],
    limit: int = Query(default=50, le=100),
    before_id: int | None = Query(default=None),
):
    return await use_case(
        current_user_id=current_user_id,
        channel_id=channel_id,
        limit=limit,
        before_id=before_id,
    )
