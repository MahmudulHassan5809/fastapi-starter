from .admin import router as user_admin_router
from .user import router as user_router

__all__ = [
    "user_router",
    "user_admin_router",
]
