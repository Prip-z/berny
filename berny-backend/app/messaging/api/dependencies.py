from typing import Annotated

from app.messaging.application.GetChannelMessagesUseCase import (
    GetChannelMessagesUseCase,
)
from app.messaging.application.SendMessagingUseCase import SendMessagingUseCase
from app.messaging.domain.ConnectionManager import ConnectionManager
from app.messaging.infrastructure.brokers import MessageBroker
from app.messaging.infrastructure.database import ScyllaDatabase
from app.messaging.infrastructure.PostgresChannelAccessValidator import (
    PostgresChannelAccesValidator,
)
from app.messaging.infrastructure.repositories import ScyllaMessageRepository
from app.shared.domain.security.TokenWrapper import JWTWrapper
from app.shared.infrastructure.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

message_broker = MessageBroker()
scylla_db = ScyllaDatabase()
connection_manager = ConnectionManager()


def get_scylla_repo() -> ScyllaMessageRepository:
    if scylla_db.session is None:
        raise RuntimeError("ScyllaDB session is not initialized. Call connect() first.")
    return ScyllaMessageRepository(scylla_db.session)


def get_message_broker() -> MessageBroker:
    return message_broker


def get_access_validator(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> PostgresChannelAccesValidator:
    return PostgresChannelAccesValidator(session)


def get_send_message_use_case(
    repo: Annotated[ScyllaMessageRepository, Depends(get_scylla_repo)],
    broker: Annotated[MessageBroker, Depends(get_message_broker)],
    access_validator: Annotated[
        PostgresChannelAccesValidator, Depends(get_access_validator)
    ],
) -> SendMessagingUseCase:
    return SendMessagingUseCase(
        repo=repo, broker=broker, access_validator=access_validator
    )


def get_validate_token():
    return JWTWrapper.decode


def get_channel_messages_use_case(
    repo: Annotated[ScyllaMessageRepository, Depends(get_scylla_repo)],
    access_validator: Annotated[
        PostgresChannelAccesValidator, Depends(get_access_validator)
    ],
) -> GetChannelMessagesUseCase:
    return GetChannelMessagesUseCase(repo, access_validator)
