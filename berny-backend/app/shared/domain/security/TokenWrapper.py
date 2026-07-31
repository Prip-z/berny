from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from app.identify.domain.exception import InvalidToken, TokenExpired
from app.shared.config import settings


class JWTWrapper:
    @staticmethod
    def encode_access(payload_id: UUID) -> str:
        EXPIRATION_TIME = datetime.now(timezone.utc) + timedelta(minutes=30)
        payload = {
            "sub": str(payload_id),
            "type": "access",
            "exp": int(EXPIRATION_TIME.timestamp()),
        }
        return jwt.encode(
            payload,
            settings.SECRET_JWT,
        )

    @staticmethod
    def encode_refresh(payload_id: UUID) -> str:
        EXPIRATION_TIME = datetime.now(timezone.utc) + timedelta(days=7)
        payload = {
            "sub": str(payload_id),
            "type": "refresh",
            "exp": int(EXPIRATION_TIME.timestamp()),
        }
        return jwt.encode(
            payload,
            settings.SECRET_JWT,
        )

    @staticmethod
    def decode(token: str) -> dict:
        if not token:
            raise InvalidToken
        try:
            data = jwt.decode(token, settings.SECRET_JWT, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise TokenExpired("Token Expired")
        except jwt.InvalidTokenError:
            raise InvalidToken("InvalidToken")
        return data
