import asyncio
from uuid import UUID

from app.messaging.domain.Message import Message
from cassandra.cluster import Session
from cassandra.query import PreparedStatement


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
            ),
        )
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, future.result)

    async def get_messages_by_channel(
        self,
        channel_id: UUID,
        time_bucket: str,
        limit: int = 50,
        before_id: int | None = None,
    ) -> list[Message]:
        loop = asyncio.get_running_loop()

        if before_id:
            query = """
                SELECT channel_id, time_bucket, message_id, sender_id, text, created_at
                FROM messages
                WHERE channel_id = ? AND time_bucket = ? AND message_id < ?
                LIMIT ?
            """
            stmt = self._session.prepare(query)
            future = self._session.execute_async(
                stmt, (channel_id, time_bucket, before_id, limit)
            )
        else:
            query = """
                SELECT channel_id, time_bucket, message_id, sender_id, text, created_at
                FROM messages
                WHERE channel_id = ? AND time_bucket = ?
                LIMIT ?
            """
            stmt = self._session.prepare(query)
            future = self._session.execute_async(stmt, (channel_id, time_bucket, limit))

        rows = await loop.run_in_executor(None, future.result)

        messages = []
        for row in rows:
            messages.append(
                Message(
                    message_id=row.message_id,
                    channel_id=row.channel_id,
                    sender_id=row.sender_id,
                    text=row.text,                        
                    created_at=row.created_at,
                )
            )
        return messages
