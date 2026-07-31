from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    @staticmethod
    @abstractmethod
    async def hash(password: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    async def check(password: str, password_hash: str) -> bool:
        pass
