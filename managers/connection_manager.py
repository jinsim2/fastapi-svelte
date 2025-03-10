from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        # room 이름을 key로, 해당 room에 연결된 WebSocket 리스트를 value로 저장
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, room: str, websocket: WebSocket):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, room: str, message: str):
        for connection in self.active_connections.get(room, []):
            await connection.send_text(message)

    def get_active_rooms(self):
        # 현재 active한 room 이름 리스트 반환
        return list(self.active_connections.keys())


# 전역 인스턴스 생성
manager = ConnectionManager()
