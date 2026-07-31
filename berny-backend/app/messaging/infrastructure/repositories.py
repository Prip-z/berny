import asyncio
from cassandra.cluster import Session
from cassandra.query import PreparedStatement
from app.messaging.domain.Message import Message


class ScyllaMessageRepository:
    def __init__(self, session: Session):
        self._session = session
        self._insert_stmt: PreparedStatement = self._session.prepare("""
            INSERT INTO messages (
                channel_id, 
                time_bucket, 
                message_id, 
                sender_id, 
                text, 
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """)

    async def save(self, message: Message) -> None:
        future = self._session.execute_async(
            self._insert_stmt,
            (
                message.channel_id,
                message.time_bucket,
                message.message_id,
                message.sender_id,
                message.text,
                message.created_at,
            )
        )
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, future.result)