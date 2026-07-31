from abc import ABC, abstractmethod

from app.identify.domain.entity.DTO import (
    SsoTokenResult,
    SsoUserInfo,
    TokenValidationResult,
)


class ISSOProvider(ABC):
    @abstractmethod
    async def get_authorization_url(
        self, state: str, nonce: str, scopes: list[str]
    ) -> str:
        pass

    @abstractmethod
    async def exchange_code_for_tokens(
        self, auth_code: str, code_verifier: str
    ) -> SsoTokenResult:
        pass

    @abstractmethod
    async def validate_token(self, access_token: str) -> TokenValidationResult:
        pass

    @abstractmethod
    async def get_user_info(self, access_token: str) -> SsoUserInfo:
        pass

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str) -> SsoTokenResult:
        pass

    @abstractmethod
    async def revoke_token(self, token: str) -> bool:
        pass

    @abstractmethod
    async def get_logout_url(
        self,
        id_token_hint: str | None = None,
        post_logout_redirect_uri: str | None = None,
    ) -> str:
        pass
