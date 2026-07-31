import httpx
from app.identify.domain.entity.DTO import (
    SsoTokenResult,
    SsoUserInfo,
    TokenValidationResult,
)
from app.identify.domain.interface.ISSOProvider import ISSOProvider


class GoogleAuth(ISSOProvider):
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
    TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"
    REVOKE_URL = "https://oauth2.googleapis.com/revoke"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_url: str,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url

    async def get_authorization_url(
        self, state: str, nonce: str, scopes: list[str]
    ) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_url,
            "response_type": "code",
            "scope": " ".join(scopes),
            "state": state,
            "nonce": nonce,
            "access_type": "offline",
            "prompt": "consent",
        }
        req = httpx.Request("GET", self.AUTH_URL, params=params)
        return str(req.url)

    async def exchange_code_for_tokens(
        self, auth_code: str, code_verifier: str
    ) -> SsoTokenResult:
        data = {
            "code": auth_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_url,
            "grant_type": "authorization_code",
            "code_verifier": code_verifier,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.TOKEN_URL, data=data)
            response.raise_for_status()
            payload = response.json()

        return SsoTokenResult(
            access_token=payload["access_token"],
            refresh_token=payload.get("refresh_token"),
            id_token=payload.get("id_token"),
            expires_in=payload.get("expires_in"),
            token_type=payload.get("token_type", "Bearer"),
        )

    async def validate_token(self, access_token: str) -> TokenValidationResult:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.TOKEN_INFO_URL, params={"access_token": access_token}
            )
            if response.status_code != 200:
                return TokenValidationResult(is_valid=False)

            payload = response.json()
            is_valid = payload.get("aud") == self.client_id
            return TokenValidationResult(
                is_valid=is_valid,
                user_id=payload.get("sub"),
                scopes=payload.get("scope", "").split(" ")
                if payload.get("scope")
                else [],
                expires_in=int(payload.get("exp", 0)),
            )

    async def get_user_info(self, access_token: str) -> SsoUserInfo:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.USER_INFO_URL, headers=headers)
            response.raise_for_status()
            payload = response.json()

        return SsoUserInfo(
            sub=payload["sub"],
            email=payload.get("email"),
            email_verified=payload.get("email_verified", False),
            given_name=payload.get("given_name"),
            family_name=payload.get("family_name"),
            picture=payload.get("picture"),
        )

    async def refresh_tokens(self, refresh_token: str) -> SsoTokenResult:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.TOKEN_URL, data=data)
            response.raise_for_status()
            payload = response.json()

            return SsoTokenResult(
                access_token=payload["access_token"],
                refresh_token=payload.get("refresh_token", refresh_token),
                id_token=payload.get("id_token"),
                expires_in=payload.get("expires_in"),
                token_type=payload.get("token_type", "Bearer"),
            )

    async def revoke_token(self, token: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.REVOKE_URL, params={"token": token})
            return response.status_code == 200

    async def get_logout_url(
        self,
        id_token_hint: str | None = None,
        post_logout_redirect_uri: str | None = None,
    ) -> str:
        base_url = "https://accounts.google.com/Logout"
        if post_logout_redirect_uri:
            params = {
                "continue": f"https://appengine.google.com/_ah/logout?continue={post_logout_redirect_uri}"
            }
            req = httpx.Request("GET", base_url, params=params)
            return str(req.url)
        return base_url
