from fastapi import APIRouter

from app.auth.deps import AnnotatedCurrentUserDep, CurrentUserDep
from app.common.deps.common import AnnotatedCommonDep
from app.common.deps.db import SessionDep
from app.common.deps.search import AnnotatedSearchClientsDep
from app.user.deps import (
    CurrentCanDeleteUser,
    CurrentCanReadUser,
    CurrentCanUpdateUser,
)
from app.user.models import UserCreate, UserOut, UserUpdate
from app.user.repository import UserRepo

router = APIRouter()


@router.post(
    "/",
    response_model=UserOut,
    status_code=201,
)
async def create_user(_user: UserCreate, *, deps: AnnotatedCommonDep):
    return await UserRepo.create(deps, obj_in=_user)


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
    dependencies=[CurrentUserDep, CurrentCanReadUser],
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
async def update_user(user_id: int, user: UserUpdate, *, deps: AnnotatedCommonDep):
    return await UserRepo.update(deps, id_=user_id, obj_in=user)


@router.delete(
    "/{user_id}",
    dependencies=[CurrentCanDeleteUser],
    status_code=204,
)
async def delete_user(user_id: int, *, deps: AnnotatedCommonDep):
    return await UserRepo.remove(deps, id_=user_id)
