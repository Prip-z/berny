from abc import ABC, abstractmethod
from uuid import UUID

from app.identify.domain.entity.User import User, UserUpdateData
from sqlalchemy.ext.asyncio import AsyncSession


class IUserRepository(ABC):
    def __init__(self, _session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def read(self, email: str) -> User:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user_id: UUID, changes: UserUpdateData) -> User | None:
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        pass
