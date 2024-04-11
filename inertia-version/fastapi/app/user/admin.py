from typing import Any, Dict, cast

from fastapi import Request
from openfga_sdk import OpenFgaClient
from sqladmin import ModelView

from app.common.deps.authz import fga_client_configuration
from app.user.fga import UserFGA, UserRole
from app.user.models import User


class UserAdminView(ModelView, model=User):
    column_exclude_list = ["hashed_password"]

    async def after_model_change(
        self, data: Dict[str, Any], model: User, is_created: bool, request: Request
    ) -> None:
        if is_created:
            user_id = cast(int, model.id)
            user_role = cast(
                UserRole, "client" if not model.is_superuser else "superuser"
            )
            async with OpenFgaClient(fga_client_configuration) as fga_client:
                await UserFGA.create_relationships(fga_client, user_id, user_role)

    async def after_model_delete(self, model: User, request: Request) -> None:
        user_id = cast(int, model.id)
        user_role = cast(UserRole, "client" if not model.is_superuser else "superuser")
        async with OpenFgaClient(fga_client_configuration) as fga_client:
            await UserFGA.delete_relationships(fga_client, user_id, user_role)
