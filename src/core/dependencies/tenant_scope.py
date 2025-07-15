from typing import Any

from dependency_injector.wiring import Provide
from fastapi import Depends, Header, HTTPException
from src.core.db import Database
from src.core.di import Container


async def tenant_scope(
    x_tenant_id: str = Header(...),
    db: Database = Depends(Provide[Container.db]),
) -> Any:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Missing tenant")

    async with db.session(tenant=x_tenant_id) as session:
        with Container.db_session.override(lambda: session):
            yield
