from datetime import datetime, timedelta
from typing import cast

from openfga_sdk import OpenFgaClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.models import AdminToken
from app.common.deps.search import StructuredSearchClient
from app.common.test_utils.utils import random_lower_string
from app.user.models import User
from app.user.tests.factory import new_default_user


async def new_admin_token(session: AsyncSession, **kwargs) -> AdminToken:
    admin_token = AdminToken(**kwargs)
    session.add(admin_token)
    await session.commit()
    await session.refresh(admin_token)
    return admin_token


async def new_default_admin_token(
    session: AsyncSession,
    fga_client: OpenFgaClient,
    search_clients: StructuredSearchClient,
    *,
    token: str | None = None,
    user: User | None = None,
    user_id: int | None = None,
    expires_in: timedelta | None = None,
):
    if user_id is not None:
        user_id_ = user_id
    elif user is not None:
        user_id_ = cast(int, user.id)
    else:
        user = await new_default_user(session, fga_client, search_clients)
        user_id_ = cast(int, user.id)
    expires_at = datetime.utcnow() + (expires_in or timedelta(minutes=15))
    token = token or random_lower_string()
    return await new_admin_token(
        session, user_id=user_id_, expires_at=expires_at, token=token
    )
