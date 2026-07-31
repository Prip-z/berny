from app.identify.domain.entity.User import User
from app.identify.domain.interface.IPasswordHasher import IPasswordHasher
from app.identify.domain.interface.IUserRepository import IUserRepository


class UserCreateUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        hasher: IPasswordHasher,
    ):
        self._user_repo = user_repo
        self._hasher = hasher

    async def __call__(self, username: str, password: str, email: str) -> User:

        password_hash = await self._hasher.hash(password)
        user = User(username=username, password_hash=password_hash, email=email)

        return await self._user_repo.create(user)
