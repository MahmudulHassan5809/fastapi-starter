from dependency_injector import containers, providers
from src.core.config import settings
from src.core.db.connector import Database
from src.modules.auth import UserAuthService
from src.modules.users import User, UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

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

    db_session = providers.Dependency(instance_of=AsyncSession)

    user_repository = providers.Factory(
        UserRepository, session_factory=db_session, model=User
    )

    user_auth_service = providers.Factory(UserAuthService, user_repository=user_repository)
