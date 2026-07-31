from app.messaging.application.SendMessagingUseCase import SendMessagingUseCase
from app.messaging.domain.ConnectionManager import ConnectionManager
from app.messaging.infrastructure.brokers import MessageBroker
from app.messaging.infrastructure.database import ScyllaDatabase
from app.messaging.infrastructure.repositories import ScyllaMessageRepository
from app.shared.domain.security.TokenWrapper import JWTWrapper

message_broker = MessageBroker()
scylla_db = ScyllaDatabase()
connection_manager = ConnectionManager()


def get_scylla_repo() -> ScyllaMessageRepository:
    if scylla_db.session is None:
        raise RuntimeError("ScyllaDB session is not initialized. Call connect() first.")
    return ScyllaMessageRepository(scylla_db.session)


def get_message_broker() -> MessageBroker:
    return message_broker


def get_send_message_use_case() -> SendMessagingUseCase:
    repo = get_scylla_repo()
    return SendMessagingUseCase(repo=repo, broker=message_broker)

def get_validate_token():
    return JWTWrapper.decode