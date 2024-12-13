from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, rooms, tasks

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
