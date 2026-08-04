import json
from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[UUID, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: UUID, subprotocol=None):
        await websocket.accept(subprotocol=subprotocol)
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: UUID):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def _send_to_users(self, target_users: list[UUID], json_message: dict):
        for target_user in target_users:
            if target_user in self.active_connections:
                for websocket in self.active_connections[target_user]:
                    await websocket.send_json(json_message)

    async def handle_broker_message(self, raw_data: str):
        data = json.loads(raw_data)
        target_user_ids = [UUID(uid) for uid in data.get("target_user_ids", [])]
        payload = data.get("payload")
        await self._send_to_users(target_users=target_user_ids, json_message=payload)
