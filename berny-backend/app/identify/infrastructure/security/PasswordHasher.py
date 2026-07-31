import asyncio

import bcrypt
from app.identify.domain.interface.IPasswordHasher import IPasswordHasher


class BCryptPasswordHasher(IPasswordHasher):
    @staticmethod
    async def hash(password: str) -> str:
        return await asyncio.to_thread(
            lambda: bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt(rounds=12)
            ).decode("utf-8")
        )

    @staticmethod
    async def check(password: str, password_hash: str) -> bool:
        def _sync_check():
            password_bytes = password.encode("utf-8")
            password_hash_bytes = password_hash.encode("utf-8")
            return bcrypt.checkpw(password_bytes, password_hash_bytes)

        return await asyncio.to_thread(_sync_check)
