import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.api_v1 import api_router_v1
from app.auth.api import router as auth_router
from app.auth.exceptions import AlreadyLoggedInException, InvalidTokenException
from app.webapp.api import webapp_router
from app.libs.inertia import InertiaMiddleware, settings as inertia_settings
from app.common.exceptions import (
    CommonDetailedException,
    already_logged_in_handler, common_error_handler, invalid_token_handler,
)
from app.core.admin import create_admin
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


inertia_assets_dir = (
    os.path.join(os.path.dirname(__file__), "..", "..", "vue", "src")
    if inertia_settings.INERTIA_ENV == "dev"
    else os.path.join(os.path.dirname(__file__), "..", "..", "vue", "dist")
)


app.add_middleware(InertiaMiddleware)

app.mount("/src", StaticFiles(directory=inertia_assets_dir), name="static")

app.include_router(auth_router, tags=["login"])
app.include_router(webapp_router, include_in_schema=False)
app.include_router(api_router_v1, prefix=settings.API_V1_STR)

create_admin(app)

app.add_exception_handler(CommonDetailedException, common_error_handler)
app.add_exception_handler(AlreadyLoggedInException, already_logged_in_handler)
app.add_exception_handler(InvalidTokenException, invalid_token_handler)
