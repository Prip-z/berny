# app/identify/api/router.py
from typing import Annotated
from uuid import UUID

from app.identify.api.dependencies import (
    get_user_create_usecase,
    get_user_delete_usecase,
    get_user_update_usecase,
    get_user_with_email_usecase,
)
from app.identify.api.schemas.AuthSchema import AuthResponse, TokenPair
from app.identify.api.schemas.UserSchema import UserCreate, UserLogin, UserResponse
from app.identify.application.user.UserCreateUseCase import UserCreateUseCase
from app.identify.application.user.UserDeleteUseCase import UserDeleteUseCase
from app.identify.application.user.UserGetWithEmailUseCase import (
    UserGetWithEmailUseCase,
)
from app.identify.application.user.UserUpdateUseCase import UserUpdateUseCase
from app.identify.domain.entity.User import UserUpdateData
from app.identify.domain.exception import (
    InvalidPassword,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.shared.domain.security.TokenWrapper import JWTWrapper
from fastapi import APIRouter, Depends, HTTPException, status

identify_router = APIRouter(prefix="/identify")


@identify_router.post(
    "/api/v1/auth/login",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def login_user(
    payload: UserLogin,
    use_case: Annotated[UserGetWithEmailUseCase, Depends(get_user_with_email_usecase)],
):
    try:
        user = await use_case(email=payload.email, password=payload.password)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except InvalidPassword:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password"
        )
    access_token = JWTWrapper.encode_access(user.user_id)
    refresh_token = JWTWrapper.encode_refresh(user.user_id)
    tokens = TokenPair(access_token=access_token, refresh_token=refresh_token)
    return AuthResponse(user=user, tokens=tokens)


@identify_router.post(
    "/api/v1/auth/registration",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserCreate,
    use_case: Annotated[UserCreateUseCase, Depends(get_user_create_usecase)],
):
    try:
        user = await use_case(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    access_token = JWTWrapper.encode_access(user.user_id)
    refresh_token = JWTWrapper.encode_refresh(user.user_id)
    tokens = TokenPair(access_token=access_token, refresh_token=refresh_token)
    return AuthResponse(user=user, tokens=tokens)


"""АДМИНКА ААААААААААААА"""


@identify_router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: UserCreate,
    use_case: Annotated[UserCreateUseCase, Depends(get_user_create_usecase)],
):
    try:
        return await use_case(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )


# @identify_router.get("/users/{email}", response_model=UserResponse)
# async def get_user(
#     email: str,
#     use_case: Annotated[UserGetUseCase, Depends(get_user_get_usecase)],
# ):
#     try:
#         return await use_case(email=email)
#     except UserNotFoundError:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )


@identify_router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdateData,
    use_case: Annotated[UserUpdateUseCase, Depends(get_user_update_usecase)],
):
    try:
        return await use_case(user_id, **user_data.model_dump(exclude_unset=True))
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )


@identify_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    use_case: Annotated[UserDeleteUseCase, Depends(get_user_delete_usecase)],
):
    try:
        await use_case(user_id=user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
