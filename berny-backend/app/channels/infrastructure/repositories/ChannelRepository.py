from uuid import UUID

from app.channels.domain.entity.Channel import Channel, ChannelType, ChannelUpdateData
from app.channels.domain.entity.ChannelMembers import ChannelMembers, UserRole
from app.channels.domain.entity.SearchResultItem import SearchResultItem
from app.channels.domain.exception import ChannelNotFound, ChatAlreadyExist
from app.channels.domain.interface.IChannelRepository import IChannelRepository
from app.channels.infrastructure.models.ChannelMembersModel import (
    ChannelMembersORM,
)
from app.channels.infrastructure.models.ChannelModel import Channel as ChannelORM
from app.identify.infrastructure.models.UserModel import User as UserORM
from sqlalchemy import String, cast, func, literal, select, union_all
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased


class ChannelRepository(IChannelRepository):
    def __init__(self, _session: AsyncSession):
        self._session = _session

    async def search_channel(
        self, search_query: str, current_user_id: UUID
    ) -> list[SearchResultItem]:
        stmt_public_channels = (
            select(
                ChannelORM.channel_id.label("id"),
                ChannelORM.name.label("title"),
                literal("public_channel").label("result_type"),
                cast(None, String).label("target_user_id"),
                func.similarity(ChannelORM.name, search_query).label("score"),
            )
            .where(ChannelORM.type == ChannelType.PUBLIC)
            .where(func.similarity(ChannelORM.name, search_query) > 0.2)
        )

        user_channel_members = aliased(ChannelMembersORM)
        direct_channel = aliased(ChannelORM)

        stmt_users = (
            select(
                direct_channel.channel_id.label("id"),
                UserORM.username.label("title"),
                literal("user_search").label("result_type"),
                cast(UserORM.user_id, String).label("target_user_id"),
                func.similarity(UserORM.username, search_query).label("score"),
            )
            .select_from(UserORM)
            .outerjoin(
                user_channel_members, user_channel_members.user_id == UserORM.user_id
            )
            .outerjoin(
                direct_channel,
                (direct_channel.channel_id == user_channel_members.channel_id)
                & (direct_channel.type == ChannelType.DIRECT)
                & (
                    direct_channel.channel_id.in_(
                        select(ChannelMembersORM.channel_id).where(
                            ChannelMembersORM.user_id == current_user_id
                        )
                    )
                ),
            )
            .where(UserORM.user_id != current_user_id)
            .where(func.similarity(UserORM.username, search_query) > 0.2)
        )

        stmt_my_chats = (
            select(
                ChannelORM.channel_id.label("id"),
                ChannelORM.name.label("title"),
                literal("my_chat").label("result_type"),
                cast(None, String).label("target_user_id"),
                func.similarity(ChannelORM.name, search_query).label("score"),
            )
            .join(
                ChannelMembersORM, ChannelMembersORM.channel_id == ChannelORM.channel_id
            )
            .where(ChannelMembersORM.user_id == current_user_id)
            .where(ChannelORM.type != ChannelType.DIRECT)
            .where(func.similarity(ChannelORM.name, search_query) > 0.2)
        )

        combined_query = union_all(
            stmt_public_channels, stmt_users, stmt_my_chats
        ).alias("search_results")

        final_stmt = select(combined_query).order_by(combined_query.c.score.desc())

        result = await self._session.execute(final_stmt)
        rows = result.mappings().all()

        return [SearchResultItem.model_validate(row) for row in rows]

    async def create_channel(self, channel: Channel) -> Channel:
        try:
            channel_orm = ChannelORM(**channel.model_dump())
            self._session.add(channel_orm)
            await self._session.flush()
        except IntegrityError:
            raise ChatAlreadyExist()
        return channel

    async def get_with_id(self, channel_id: UUID) -> Channel:
        channel = await self._session.get(ChannelORM, channel_id)
        if not channel:
            raise ChannelNotFound()
        return Channel.model_validate(channel)

    async def update_channel(
        self, channel_id: UUID, changes: ChannelUpdateData
    ) -> Channel | None:
        channel_orm = await self._session.get(ChannelORM, channel_id)
        if not channel_orm:
            raise ChannelNotFound()

        update_dict = changes.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(channel_orm, key, value)

        return Channel.model_validate(channel_orm)

    async def delete_channel(self, channel_id: UUID) -> bool:
        channel = await self._session.get(ChannelORM, channel_id)
        if channel:
            await self._session.delete(channel)
            return True
        return False

    async def add_member(
        self, channel_id: UUID, user_id: UUID, role: UserRole | None = UserRole.READER
    ) -> ChannelMembers:
        member_orm = ChannelMembersORM(
            channel_id=channel_id,
            user_id=user_id,
            role=role,
        )
        self._session.add(member_orm)
        await self._session.flush()
        return ChannelMembers.model_validate(member_orm)

    async def remove_member(self, channel_id: UUID, user_id: UUID) -> bool:
        member_orm = await self._session.get(ChannelMembersORM, (channel_id, user_id))
        if member_orm:
            await self._session.delete(member_orm)
            return True
        return False

    async def get_members(self, channel_id: UUID) -> list[ChannelMembers]:
        stmt = select(ChannelMembersORM).where(
            ChannelMembersORM.channel_id == channel_id
        )
        result = await self._session.execute(stmt)
        members_orm = result.scalars().all()
        return [ChannelMembers.model_validate(m) for m in members_orm]

    async def is_member(self, channel_id: UUID, user_id: UUID) -> bool:
        member_orm = await self._session.get(ChannelMembersORM, (channel_id, user_id))
        return member_orm is not None
