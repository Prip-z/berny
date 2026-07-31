from uuid import UUID

from app.identify.domain.exception import UserNotFoundError
from app.identify.domain.interface.IUserRepository import IUserRepository


class UserDeleteUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
    ):
        self._user_repo = user_repo

    async def __call__(self, user_id: UUID) -> bool:
        result = await self._user_repo.delete(user_id)
        if not result:
            raise UserNotFoundError
        else:
            return True
