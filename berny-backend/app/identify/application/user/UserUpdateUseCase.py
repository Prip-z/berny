from datetime import datetime
from uuid import UUID

from app.identify.domain.entity.User import User, UserUpdateData
from app.shared.domain.interfaces.IPasswordHasher import IPasswordHasher
from app.identify.domain.interface.IUserRepository import IUserRepository


class UserUpdateUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        hasher: IPasswordHasher,
    ):
        self._user_repo = user_repo
        self._hasher = hasher

    async def __call__(
        self,
        user_id: UUID,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        last_seen: datetime | None = None,
    ) -> User | None:
        password_hash = self._hasher.hash(password) if password else None

        changes = UserUpdateData(
            email=email,
            password_hash=password_hash,
            username=username,
            last_seen=last_seen,
        )

        return await self._user_repo.update(user_id, changes)
