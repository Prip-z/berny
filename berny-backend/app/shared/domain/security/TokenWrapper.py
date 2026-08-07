from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from app.identify.domain.exception import InvalidToken, TokenExpired
from app.shared.config import settings


class JWTWrapper:
    @staticmethod
    def encode_access(payload_id: UUID) -> str:
        EXPIRATION_TIME = datetime.now(timezone.utc) + timedelta(minutes=720)
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
    def decode(token: str) -> UUID:
        if not token:
            raise InvalidToken
        try:
            data = jwt.decode(token, settings.SECRET_JWT, algorithms=["HS256"])
            user_id = data.get("sub") or data.get("user_id") or data.get("id")
            if not user_id:
                raise InvalidToken("User ID not found in token")
            return UUID(str(user_id))
        except jwt.ExpiredSignatureError:
            raise TokenExpired("Token Expired")
        except (jwt.InvalidTokenError, ValueError, TypeError):
            raise InvalidToken("InvalidToken")
