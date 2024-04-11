from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

from fastapi import APIRouter, Request, UploadFile
from starlette.responses import RedirectResponse

from app.auth.deps import AnnotatedCurrentUserDep, CurrentUserDep
from app.auth.utils.auth import create_access_token
from app.common.deps.common import AnnotatedCommonDep
from app.common.deps.db import SessionDep
from app.common.deps.search import AnnotatedSearchClientsDep
from app.core.config import settings
from app.user.deps import (
    CurrentCanDeleteUser,
    CurrentCanReadUser,
    CurrentCanUpdateUser, UserExists,
)
from app.user.exceptions import EmailAlreadyRegisteredException, PasswordNotStrongException
from app.user.models import UserCreate, UserOut, UserUpdate
from app.user.repository import UserRepo

router = APIRouter()


@router.post(
    "/",
    status_code=201,
)
async def create_user(_user: UserCreate, *, deps: AnnotatedCommonDep):
    try:
        user = await UserRepo.create(deps, obj_in=_user)
        token = create_access_token({'email': user.email})
        response = RedirectResponse(url=f"/app", status_code=303)
        response.set_cookie(key="token", value=token, httponly=True, samesite=None, secure=True, expires=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return response
    except (EmailAlreadyRegisteredException, PasswordNotStrongException) as exc:
        response = RedirectResponse(url=f"/signup", status_code=303)
        response.set_cookie(key="error", value=exc.message, httponly=True, samesite=None, secure=True, expires=3)
        return response



@router.get("/", response_model=list[UserOut])
async def search_users(
    query: str = "",
    offset: int = 0,
    *,
    search: AnnotatedSearchClientsDep,
    user: AnnotatedCurrentUserDep,
):
    return search.user.get_search_result_hits(query, offset, current_user=user)


@router.get("/me", response_model=UserOut)
async def get_user_me(
    *,
    current_user: AnnotatedCurrentUserDep,
):
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserOut,
    dependencies=[CurrentUserDep, UserExists, CurrentCanReadUser],
)
async def get_user_by_id(
    user_id: int,
    *,
    session: SessionDep,
):
    return await UserRepo.get(session, id_=user_id)


@router.patch(
    "/{user_id}",
    response_model=UserOut,
    status_code=201,
    dependencies=[CurrentCanUpdateUser],
)
async def update_user(request: Request, user_id: int, user: UserUpdate, *, deps: AnnotatedCommonDep):
    referer = request.headers.get("Referer")
    parsed_referer_url = urlparse(referer)
    request_from = parsed_referer_url.path
    response = RedirectResponse(url=str(request_from), status_code=303)
    try:
        await UserRepo.update(deps, id_=user_id, obj_in=user)
        response.set_cookie(key="message", value="user.update_success", httponly=True, samesite=None, secure=True,
                        expires=3)
    except (EmailAlreadyRegisteredException, PasswordNotStrongException) as exc:
        response.set_cookie(key="error", value=exc.message, httponly=True, samesite=None, secure=True,
                        expires=3)
    return response


@router.post(
    "/{user_id}/avatar",
    status_code=201,
    dependencies=[CurrentCanUpdateUser],
)
async def set_user_avatar(user_id: int, avatar: UploadFile, *, session: SessionDep):
    await UserRepo.set_avatar_url(session, id_=user_id, avatar=avatar)


@router.delete(
    "/{user_id}",
    dependencies=[CurrentCanDeleteUser],
    status_code=204,
)
async def delete_user(user_id: int, *, deps: AnnotatedCommonDep):
    return await UserRepo.remove(deps, id_=user_id)
