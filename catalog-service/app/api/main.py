from fastapi import APIRouter

from app.api.routes import quests, rewards, utils

api_router = APIRouter()
api_router.include_router(quests.router, prefix="/quests", tags=["quests"])
api_router.include_router(rewards.router, prefix="/rewards", tags=["rewards"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
