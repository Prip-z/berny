from typing import Annotated
from uuid import UUID

from app.shared.domain.security.TokenWrapper import JWTWrapper
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/identify/api/v1/auth/login")


def get_current_user_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    token_data = JWTWrapper.decode(token)
    return token_data
