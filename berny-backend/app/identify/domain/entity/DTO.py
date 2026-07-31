from dataclasses import dataclass


@dataclass
class SsoTokenResult:
    access_token: str
    token_type: str = "Bearer"
    expires_in: int | None = None
    refresh_token: str | None = None
    id_token: str | None = None


@dataclass
class TokenValidationResult:
    is_valid: bool
    user_id: str | None = None
    scopes: list[str] | None = None
    expires_in: int | None = None


@dataclass
class SsoUserInfo:
    sub: str
    email: str | None = None
    email_verified: bool = False
    given_name: str | None = None
    family_name: str | None = None
    picture: str | None = None
