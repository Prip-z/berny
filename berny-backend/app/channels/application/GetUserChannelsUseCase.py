from uuid import UUID

from app.channels.domain.dto.UserChannel import UserChannel
from app.channels.domain.interface.IChannelRepository import IChannelRepository


class GetUserChannelsUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo

    async def __call__(self, current_user_id: UUID) -> list[UserChannel]:
        return await self._channel_repo.get_user_channels(current_user_id)
