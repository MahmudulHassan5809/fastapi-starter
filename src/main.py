from fastapi import FastAPI
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.middleware.response_middleware import CustomResponseMiddleware
from src.core.middleware.error_handler_middleware import CustomErrorHandler
from src.api.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
    contact={
        "email": settings.SUPER_USER_EMAIL,
    }
)

origins = ["*"]



app.add_middleware(CustomResponseMiddleware)

app.include_router(api_router, prefix=f"{settings.API_V1_STR}")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.middleware("http")(CustomErrorHandler())