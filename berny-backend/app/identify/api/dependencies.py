from typing import Annotated

from app.identify.application.user.UserCreateUseCase import UserCreateUseCase
from app.identify.application.user.UserDeleteUseCase import UserDeleteUseCase
from app.identify.application.user.UserGetUseCase import UserGetUseCase
from app.identify.application.user.UserUpdateUseCase import UserUpdateUseCase
from app.identify.domain.interface.IPasswordHasher import IPasswordHasher
from app.identify.domain.interface.IUserRepository import IUserRepository
from app.identify.infrastructure.database import get_db
from app.identify.infrastructure.repositories.PostgresUserRepository import (
    PostgresUserRepository,
)
from app.identify.infrastructure.security.PasswordHasher import BCryptPasswordHasher
from fastapi import Depends
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


def get_user_get_usecase(
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
    hasher: Annotated[IPasswordHasher, Depends(get_hasher)],
) -> UserGetUseCase:
    return UserGetUseCase(user_repo, hasher)


def get_user_update_usecase(
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
    hasher: Annotated[IPasswordHasher, Depends(get_hasher)],
) -> UserUpdateUseCase:
    return UserUpdateUseCase(user_repo, hasher=hasher)


def get_user_delete_usecase(
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
) -> UserDeleteUseCase:
    return UserDeleteUseCase(user_repo)
