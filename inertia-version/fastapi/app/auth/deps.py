from datetime import datetime
from typing import Annotated, Union, cast

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer as OAuth2PasswordBearer_
from jose import JWTError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.exceptions import AlreadyLoggedInException, InvalidTokenException
from app.auth.models import AdminToken
from app.auth.utils.auth import get_token_content
from app.common.deps.db import SessionDep
from app.common.exceptions import NotFoundException
from app.user.models import User
from app.user.repository import UserRepo


class OAuth2PasswordBearer(OAuth2PasswordBearer_):
    def __init__(
        self,
        token_url: str,
    ) -> None:
        super().__init__(
            tokenUrl=token_url,
        )

    async def __call__(self, request: Request) -> Union[str, None]:
        token = request.cookies.get("token", None)
        return token


reusable_oauth2 = OAuth2PasswordBearer(token_url="/api/login")
AnnotatedTokenDep = Annotated[Union[str, None], Depends(reusable_oauth2)]


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
    if token is None:
        raise InvalidTokenException()
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


async def redirect_if_already_logged_in(
    *, token: AnnotatedTokenDep, session: SessionDep
) -> None:
    try:
        await get_current_user(token=token, session=session)
        raise AlreadyLoggedInException()
    except InvalidTokenException:
        pass


RedirectIfAlreadyLoggedInDep = Depends(redirect_if_already_logged_in)


async def get_current_user_or_none(
    *, token: AnnotatedTokenDep, session: SessionDep
) -> Union[User, None]:
    try:
        return await get_current_user(token=token, session=session)
    except InvalidTokenException:
        return None


AnnotatedCurrentUserOrNoneDep = Annotated[
    Union[User, None], Depends(get_current_user_or_none)
]
