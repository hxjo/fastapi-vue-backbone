from typing import cast

from fastapi import Depends

from app.auth.deps import AnnotatedCurrentUserDep
from app.common.deps.authz import AnnotatedFGAClientDep
from app.common.deps.db import SessionDep
from app.common.exceptions import ForbiddenException
from app.user.fga import UserFGA
from app.user.repository import UserRepo


async def check_user_exists(user_id: int, *, session: SessionDep) -> None:
    await UserRepo.get(session, user_id)


UserExists = Depends(check_user_exists)


async def check_can_update_user(
    user_id: int, *, user: AnnotatedCurrentUserDep, fga_client: AnnotatedFGAClientDep
) -> None:
    if not await UserFGA.can_update(fga_client, cast(int, user.id), user_id):
        raise ForbiddenException(target="user")


CurrentCanUpdateUser = Depends(check_can_update_user)


async def check_can_delete_user(
    user_id: int, *, user: AnnotatedCurrentUserDep, fga_client: AnnotatedFGAClientDep
) -> None:
    if not await UserFGA.can_delete(fga_client, cast(int, user.id), user_id):
        raise ForbiddenException(target="user")


CurrentCanDeleteUser = Depends(check_can_delete_user)


async def check_can_read_user(
    user_id: int, *, user: AnnotatedCurrentUserDep, fga_client: AnnotatedFGAClientDep
) -> None:
    if not await UserFGA.can_read(fga_client, cast(int, user.id), user_id):
        raise ForbiddenException(target="user")


CurrentCanReadUser = Depends(check_can_read_user)
