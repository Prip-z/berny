from uuid import UUID

from app.channels.infrastructure.models.ChannelMembersModel import ChannelMembersORM
from app.messaging.domain.interfaces.IChannelAccessValidator import (
    IChannelAccessValidator,
)
from sqlalchemy import select


class PostgresChannelAccesValidator(IChannelAccessValidator):
    def __init__(self, _session):
        self._session = _session

    async def can_send_message(self, user_id: UUID, channel_id: UUID) -> bool:
        query = select(ChannelMembersORM).where(
            ChannelMembersORM.channel_id == channel_id,
            ChannelMembersORM.user_id == user_id,
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_channel_members_ids(self, channel_id: UUID) -> list[UUID]:
        query = select(ChannelMembersORM.user_id).where(
            ChannelMembersORM.channel_id == channel_id
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())