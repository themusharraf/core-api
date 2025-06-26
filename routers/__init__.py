from fastapi import APIRouter
from routers.user import router as user_router
from routers.auth import router as auth_router

router = APIRouter(
    prefix="/api/v1",
)
router.include_router(auth_router)
router.include_router(user_router)
