from datetime import datetime
from typing import Annotated, cast

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.exceptions import InvalidTokenException
from app.auth.models import AdminToken
from app.auth.utils.auth import get_token_content
from app.common.deps.db import SessionDep
from app.common.exceptions import NotFoundException
from app.user.models import User
from app.user.repository import UserRepo

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login")
AnnotatedTokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_user_from_admin_token(
    session: AsyncSession, req_token: str
) -> User | None:
    stmt = select(AdminToken).where(
        AdminToken.token == req_token, AdminToken.expires_at > datetime.utcnow()
    )
    res = await session.exec(stmt)
    db_token = res.first()
    if db_token is None:
        return None
    user = await UserRepo.get(session, db_token.user_id)
    if not user.is_superuser:
        return None
    return user


async def get_current_user(*, token: AnnotatedTokenDep, session: SessionDep) -> User:
    try:
        admin_user_overrides = await get_user_from_admin_token(session, token)
        if admin_user_overrides is not None:
            return admin_user_overrides

        payload = get_token_content(token)
        email = payload.get("email", None)
        if email is None:
            raise InvalidTokenException()
    except JWTError as exc:
        raise InvalidTokenException() from exc

    try:
        db_user = await UserRepo.get_by_email(session, email=cast(str, email))
    except NotFoundException as exc:
        raise InvalidTokenException() from exc
    return db_user


CurrentUserDep = Depends(get_current_user)
AnnotatedCurrentUserDep = Annotated[User, CurrentUserDep]
