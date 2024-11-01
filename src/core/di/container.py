from dependency_injector import containers, providers

from src.core.config import settings
from src.core.db.connector import Database
from src.modules.auth.service import AuthService
from src.modules.users.models import User
from src.modules.users.repository import UserRepository
from src.modules.users.services import AdminUserService, UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.modules.auth.controller",
            "src.modules.users.controllers.user",
            "src.modules.users.controllers.admin",
        ]
    )
    db = providers.Resource(
        Database,
        db_url=settings.DATABASE_URL,
    )

    user_repository = providers.Factory(
        UserRepository, session_factory=db.provided.session, model=User
    )
    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)

    admin_user_service = providers.Factory(
        AdminUserService, user_repository=user_repository
    )
