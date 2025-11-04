from fastapi import APIRouter
from app.api.endpoints import comment

api_router = APIRouter()
api_router.include_router(comment.router)
