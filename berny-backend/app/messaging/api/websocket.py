import json
import traceback
from typing import Annotated, Any

from app.identify.domain.exception import InvalidToken
from app.messaging.api.dependencies import (
    connection_manager,
    get_send_message_use_case,
    get_validate_token,
)
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws")


@router.websocket("/")
async def new_message(
    websocket: WebSocket,
    use_case: Annotated[Any, Depends(get_send_message_use_case)],
    jwt_validator: Annotated[Any, Depends(get_validate_token)],
):
    subprotocol = websocket.headers.get("sec-websocket-protocol")
    try:
        user_id = jwt_validator(subprotocol)
    except InvalidToken:
        await websocket.close(code=1008)
        return
    await connection_manager.connect(
        websocket=websocket, subprotocol=subprotocol, user_id=user_id
    )
    try:
        while True:
            raw_data = await websocket.receive_text()
            event = json.loads(raw_data)

            if event.get("type") == "NEW_MESSAGE":
                payload = event.get("payload", {})
                try:
                    await use_case(
                        sender_id=int(user_id),
                        channel_id=payload.get("channel_id", 1),
                        text=payload.get("text", ""),
                    )
                except Exception:
                    print("ОШИБКА ПРИ СОХРАНЕНИИ:")
                    traceback.print_exc()

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, user_id=user_id)
        disconnect_envelope = {
            "type": "USER_DISCONNECTED",
            "payload": {"client_id": user_id},
        }
        await connection_manager.send_to_users(disconnect_envelope)
