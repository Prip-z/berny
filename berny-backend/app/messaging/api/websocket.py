import json
import traceback

from app.messaging.api.dependencies import connection_manager, get_send_message_use_case
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws")


@router.websocket("/{client_id}")
async def new_message(
    websocket: WebSocket, client_id: str, use_case=Depends(get_send_message_use_case)
):
    await connection_manager.connect(websocket)
    try:
        while True:
            raw_data = await websocket.receive_text()
            event = json.loads(raw_data)

            if event.get("type") == "NEW_MESSAGE":
                payload = event.get("payload", {})
                try:
                    await use_case(
                        sender_id=int(client_id),
                        channel_id=payload.get("channel_id", 1),
                        text=payload.get("text", ""),
                    )
                except Exception:
                    print("ОШИБКА ПРИ СОХРАНЕНИИ:")
                    traceback.print_exc()

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        disconnect_envelope = {
            "type": "USER_DISCONNECTED",
            "payload": {"client_id": client_id},
        }
        await connection_manager.broadcast(disconnect_envelope)
