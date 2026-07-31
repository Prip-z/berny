from app.identify.domain.entity.User import User
from app.identify.domain.exception import InvalidPassword, UserNotFoundError
from app.identify.domain.interface.IPasswordHasher import IPasswordHasher
from app.identify.domain.interface.IUserRepository import IUserRepository


class UserGetUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        _hasher: IPasswordHasher,
    ):
        self._user_repo = user_repo
        self._hasher = _hasher

    async def __call__(self, email, password) -> User:
        result = await self._user_repo.read(email)
        if not result:
            raise UserNotFoundError

        password_status = await self._hasher.check(password, result.password_hash)  # type: ignore
        if not (password_status):
            raise InvalidPassword

        return result
