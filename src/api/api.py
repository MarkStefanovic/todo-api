import fastapi

from src.api import routes

__all__ = ("router",)

router = fastapi.APIRouter()
router.include_router(routes.auth.router, tags=["auth"], prefix="/auth")
router.include_router(routes.todos.router, tags=["todos"], prefix="/todos")
