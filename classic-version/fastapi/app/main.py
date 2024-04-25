from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api_v1 import api_router_v1
from app.auth.api import router as auth_router
from app.common.exceptions import CommonDetailedException, common_error_handler
from app.core.admin import create_admin
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, tags=["login"])
app.include_router(api_router_v1, prefix=settings.API_V1_STR)

create_admin(app)

app.add_exception_handler(CommonDetailedException, common_error_handler)  # type: ignore[arg-type]
