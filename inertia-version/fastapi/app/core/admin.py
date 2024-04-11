from datetime import timedelta
from typing import Any

from fastapi import FastAPI
from fastapi.requests import Request
from jose import JWTError
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.admin import TokenAdminView
from app.auth.utils.auth import (
    create_access_token,
    get_token_content,
    verify_password_against_hash,
)
from app.common.exceptions import NotFoundException
from app.core.config import settings
from app.core.sync_db import engine
from app.user.admin import UserAdminView
from app.user.repository import UserRepo


def create_admin(app: FastAPI) -> None:
    admin = Admin(
        app,
        engine=engine,
        title=settings.PROJECT_NAME,
        authentication_backend=authentication_backend,
    )
    admin.add_view(TokenAdminView)
    admin.add_view(UserAdminView)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request, *args: Any, **kwargs: Any) -> bool:
        form = await request.form()
        db_url = settings.SQLALCHEMY_DATABASE_URI.unicode_string()  # type: ignore
        engine_ = create_async_engine(db_url, echo=settings.DEBUG_SQL)
        async with AsyncSession(engine_) as session:
            email, password = form["username"], form["password"]
            if not isinstance(email, str) or not isinstance(password, str):
                return False
            try:
                db_user = await UserRepo.get_by_email(session, email=email)
            except NotFoundException:
                return False

            if not verify_password_against_hash(
                password=password, hashed_password=db_user.hashed_password
            ):
                return False

            if not db_user.is_superuser:
                return False

            token = create_access_token(
                data={"id": db_user.id, "is_superuser": True},
                expires_delta=timedelta(hours=24),
            )
            request.session.update({"token": token})

            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        try:
            decoded_token = get_token_content(token)
        except JWTError:
            return False

        if not decoded_token.get("is_superuser", False):
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
