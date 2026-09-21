from fastapi import APIRouter

from app.api.routes.transfer import router as transfers_router

api_router = APIRouter()

api_router.include_router(transfers_router)