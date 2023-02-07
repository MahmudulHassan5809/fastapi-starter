from starlette.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

class CustomErrorHandler():
    async def __call__(self, request: Request, call_next):
        try:
            return await call_next(request)
        except SQLAlchemyError as exc:
            return JSONResponse(
                status_code=400, 
                content={
                    'status': 400,
                    'message': str(exc.__dict__['orig']),
                    'meta': None
                }
            )
        except Exception as exc:
            return JSONResponse(status_code=500, content={'reason': str(exc)})