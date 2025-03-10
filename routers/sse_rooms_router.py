# routers/sse_rooms_router.py
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import asyncio
import json

from managers.connection_manager import manager

router = APIRouter(prefix="/api/sse/rooms")

async def event_generator():
    """
    매 1초마다 현재 활성 채팅방 목록을 확인하고,
    변경된 경우 JSON 문자열로 이벤트를 생성합니다.
    """
    last_rooms = None
    while True:
        # ConnectionManager의 active_connections에서 방 목록을 가져옴
        current_rooms = manager.get_active_rooms()  # 예: ["room1", "room2", "test"]
        # 목록이 변경되었을 때만 이벤트 전송
        if current_rooms != last_rooms:
            last_rooms = current_rooms.copy()
            # JSON 문자열로 변환하여 이벤트 데이터 구성
            event_data = json.dumps(current_rooms)
            yield f"data: {event_data}\n\n"
        await asyncio.sleep(1)

@router.get("/")
async def sse_rooms_endpoint(request: Request):
    """
    클라이언트에 SSE 스트림을 제공하는 엔드포인트.
    클라이언트가 연결을 끊으면 스트림을 종료합니다.
    """
    async def event_stream():
        async for event in event_generator():
            if await request.is_disconnected():
                break
            yield event

    return StreamingResponse(event_stream(), media_type="text/event-stream")
