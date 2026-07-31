from uuid import UUID

from app.channels.domain.entity.SearchResultItem import SearchResultItem
from app.channels.domain.interface.IChannelRepository import IChannelRepository


class SearchChannelUseCase:
    def __init__(self, channel_repo: IChannelRepository):
        self._channel_repo = channel_repo
    
    async def __call__(self, current_user_id: UUID, search_query: str) -> list[SearchResultItem]:
        return await self._channel_repo.search_channel(search_query, current_user_id)