from app.identify.domain.entity.User import User
from app.identify.domain.exception import UserNotFoundError
from app.identify.domain.interface.IUserRepository import IUserRepository


class UserGetWithIDUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
    ):
        self._user_repo = user_repo

    async def __call__(self, user_id) -> User:
        result = await self._user_repo.read_with_id(user_id)
        if not result:
            raise UserNotFoundError
        return result
