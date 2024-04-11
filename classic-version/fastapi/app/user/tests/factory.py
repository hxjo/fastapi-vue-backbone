from typing import cast

from openfga_sdk import OpenFgaClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.utils.auth import get_password_hash
from app.common.deps.search import StructuredSearchClient
from app.common.test_utils.utils import (
    random_email,
    random_lower_string,
    random_upload_file,
)
from app.user.fga import UserFGA, UserRole
from app.user.models import User
from app.user.search import UserSearch


async def new_user(
    session: AsyncSession,
    fga_client: OpenFgaClient,
    user_search: UserSearch,
    **kwargs,
):
    user = User(**kwargs)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    user_id = cast(int, user.id)

    role = cast(UserRole, "client" if not user.is_superuser else "superuser")
    await UserFGA.create_relationships(fga_client, user_id, role)
    user_search.add_documents([user])

    return user


async def new_default_user(
    session: AsyncSession,
    fga_client: OpenFgaClient,
    search_clients: StructuredSearchClient,
    *,
    email: str | None = None,
    username: str | None = None,
    password: str | None = None,
    avatar_file_name: str | None = None,
    is_active: bool = True,
    is_superuser: bool = False,
):
    avatar_url = random_upload_file(avatar_file_name) if avatar_file_name else None
    hashed_password = (
        get_password_hash(password)
        if password
        else get_password_hash("secure_Password91")
    )
    return await new_user(
        session,
        fga_client,
        search_clients.user,
        email=random_email() if not email else email,
        username=random_lower_string() if not username else username,
        hashed_password=hashed_password,
        is_active=is_active,
        is_superuser=is_superuser,
        avatar_url=avatar_url,
    )
