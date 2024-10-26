from dependency_injector import containers, providers

from src.core.config import settings
from src.core.db.connector import Database


class Container(containers.DeclarativeContainer):
    db = providers.Resource(
        Database,
        db_url=settings.DATABASE_URL,
    )
