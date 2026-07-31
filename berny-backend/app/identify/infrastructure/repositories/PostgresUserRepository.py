from uuid import UUID

import sqlalchemy
from app.identify.domain.entity.User import User, UserUpdateData
from app.identify.domain.exception import UserAlreadyExistsError, UserNotFoundError
from app.identify.domain.interface.IUserRepository import IUserRepository
from app.identify.infrastructure.models.UserModel import User as UserORM
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def read(self, email: str) -> User:
        query = sqlalchemy.select(UserORM).where(UserORM.email == email)
        user = await self._session.scalar(query)
        if not user:
            raise UserNotFoundError()
        return User.model_validate(user)

    async def create(self, user: User) -> User:
        try:
            user_orm = UserORM(**user.model_dump())
            self._session.add(user_orm)
            await self._session.flush()
            return user
        except IntegrityError:
            raise UserAlreadyExistsError(
                f"User with username '{user.username}' already exists"
            )

    async def update(self, user_id: UUID, changes: UserUpdateData) -> User:
        user_orm = await self._session.get(UserORM, user_id)
        if not user_orm:
            raise UserNotFoundError()

        update_dict = changes.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(user_orm, key, value)

        return User.model_validate(user_orm)

    async def delete(self, user_id: UUID) -> bool:
        user = await self._session.get(UserORM, user_id)
        if user:
            await self._session.delete(user)
            return True
        else:
            return False
