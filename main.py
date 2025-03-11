from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from routers import answer_router, question_router, websocket_router, room_router, sse_rooms_router

from config import settings

app = FastAPI()

origins = [
    "http://localhost:5173",    # 또는 "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/info")
def read_info():
    return {
        "Database URL": settings.database_url,
        "Secret Key": settings.secret_key,
        "API Key" : settings.api_key,
    }


app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(websocket_router.router)
app.include_router(room_router.router)
app.include_router(sse_rooms_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")