from datetime import datetime, timedelta, timezone
from typing import Annotated
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, Request, UploadFile
from starlette.responses import RedirectResponse

from app.auth.deps import AnnotatedCurrentUserDep, CurrentUserDep
from app.auth.utils.auth import add_token_to_response, create_access_token
from app.common.deps.common import AnnotatedCommonDep
from app.common.deps.db import SessionDep
from app.common.deps.inertia import InertiaDep
from app.common.deps.search import AnnotatedSearchClientsDep
from app.core.config import settings
from app.libs.inertia import InertiaRenderer
from app.user.deps import (
    CurrentCanDeleteUser,
    CurrentCanReadUser,
    CurrentCanUpdateUser,
    UserExists,
)
from app.user.exceptions import (
    EmailAlreadyRegisteredException,
    PasswordNotStrongException,
)
from app.user.models import UserCreate, UserOut, UserUpdate
from app.user.repository import UserRepo

router = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=None
)
async def create_user(user: UserCreate, *, inertia: InertiaDep,  deps: AnnotatedCommonDep) -> RedirectResponse:
    try:
        user_ = await UserRepo.create(deps, obj_in=user)
        response = RedirectResponse(url="/app", status_code=303)
        response = add_token_to_response(response, email=user_.email)
        return response
    except (EmailAlreadyRegisteredException, PasswordNotStrongException) as exc:
        inertia.flash(exc.message, category="error")
        response = RedirectResponse(url="/signup", status_code=303)
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
async def update_user(
    request: Request, user_id: int, user: UserUpdate, *, deps: AnnotatedCommonDep, inertia: InertiaDep
):
    referer = request.headers.get("Referer")
    parsed_referer_url = urlparse(referer)
    request_from = parsed_referer_url.path
    response = RedirectResponse(url=str(request_from), status_code=303)
    try:
        await UserRepo.update(deps, id_=user_id, obj_in=user)
        inertia.flash("user.update_success", category="message")

    except (EmailAlreadyRegisteredException, PasswordNotStrongException) as exc:
        inertia.flash(exc.message, category="error")

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
