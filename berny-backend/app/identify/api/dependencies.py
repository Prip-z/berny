from typing import Annotated

from app.identify.application.user.UserCreateUseCase import UserCreateUseCase
from app.identify.application.user.UserDeleteUseCase import UserDeleteUseCase
from app.identify.application.user.UserGetWithEmailUseCase import (
    UserGetWithEmailUseCase,
)
from app.identify.application.user.UserGetWithIDUseCase import UserGetWithIDUseCase
from app.identify.application.user.UserUpdateUseCase import UserUpdateUseCase
from app.identify.domain.interface.IPasswordHasher import IPasswordHasher
from app.identify.domain.interface.IUserRepository import IUserRepository
from app.identify.infrastructure.database import get_db
from app.identify.infrastructure.repositories.PostgresUserRepository import (
    PostgresUserRepository,
)
from app.identify.infrastructure.security.PasswordHasher import BCryptPasswordHasher
from app.shared.domain.security.TokenWrapper import JWTWrapper
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession


def get_user_repo(session: Annotated[AsyncSession, Depends(get_db)]) -> IUserRepository:
    return PostgresUserRepository(session)


def get_hasher() -> IPasswordHasher:
    return BCryptPasswordHasher()


def get_user_create_usecase(
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
    hasher: Annotated[IPasswordHasher, Depends(get_hasher)],
) -> UserCreateUseCase:
    return UserCreateUseCase(user_repo=user_repo, hasher=hasher)


def get_user_with_email_usecase(
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
    hasher: Annotated[IPasswordHasher, Depends(get_hasher)],
) -> UserGetWithEmailUseCase:
    return UserGetWithEmailUseCase(user_repo, hasher)

def get_user_with_id_usecase(
        user_repo: Annotated[IUserRepository, Depends(get_user_repo),]
) -> UserGetWithIDUseCase:
    return UserGetWithIDUseCase(user_repo)
def get_user_update_usecase(
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
    hasher: Annotated[IPasswordHasher, Depends(get_hasher)],
) -> UserUpdateUseCase:
    return UserUpdateUseCase(user_repo, hasher=hasher)


def get_user_delete_usecase(
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
) -> UserDeleteUseCase:
    return UserDeleteUseCase(user_repo)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/identify/api/v1/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    use_case: Annotated[UserGetWithIDUseCase, Depends(get_user_with_id_usecase)],
):
    token_data = JWTWrapper.decode(token)
    user_id_from_token = token_data.get("sub")
    return use_case(user_id_from_token)
