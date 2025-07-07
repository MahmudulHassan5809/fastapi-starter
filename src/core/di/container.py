from dependency_injector import containers, providers
from src.core.config import settings
from src.core.db.connector import Database
from src.modules.auth import UserAuthService
from src.modules.users import User, UserRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.modules.auth.controllers.user",
        ]
    )

    db = providers.Resource(
        Database,
        db_url=settings.DATABASE_URL,
    )

    user_repository = providers.Factory(
        UserRepository, session_factory=db.provided.session, model=User
    )

    user_auth_service = providers.Factory(UserAuthService, user_repository=user_repository)
