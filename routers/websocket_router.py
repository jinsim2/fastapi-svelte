from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from managers.connection_manager import manager  # 새로 추가한 모듈

router = APIRouter(prefix="/api/ws")


@router.websocket("/chat/{room}")
async def chat(websocket: WebSocket, room: str):
    await manager.connect(room, websocket)
    try:
        await manager.send_personal_message(f"Welcome to room {room}", websocket)
        while True:
            data = await websocket.receive_text() # 클라이언트가 보낸 JSON 문자열을 받음
            # 그대로 같은 방의 모든 클라이언트에게 브로드캐스트
            await manager.broadcast(room, data)
    except WebSocketDisconnect:
        manager.disconnect(room, websocket)
        await manager.broadcast(room, f"Client disconnected from room {room}")