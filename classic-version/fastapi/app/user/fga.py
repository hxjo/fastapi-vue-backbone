from typing import List, Literal, LiteralString, Optional

from openfga_sdk import OpenFgaClient
from openfga_sdk.client.models.tuple import ClientTuple
from app.common.fga import BaseFGA

AllowedUserRelations = Literal["can_read", "can_update", "can_delete"]

UserRole = Literal["superuser", "user"]


class UserFGA(BaseFGA):
    object_name = "user_self"

    @staticmethod
    def get_tuples(user_id: int, role: str, object_id: int) -> List[ClientTuple]:
        return [
            ClientTuple(
                user=f"user:{user_id}",
                relation=role,
                object="app:app",
            ),
            ClientTuple(
                user=f"user:{user_id}",
                relation="self_user",
                object=f"user_self:{user_id}",
            ),
            ClientTuple(
                user="app:app",
                relation="parent_app",
                object=f"user_self:{user_id}",
            ),
        ]

    @classmethod
    async def create_relationships(
        cls,
        fga_client: OpenFgaClient,
        user_id: int,
        role: LiteralString,
        object_id: Optional[int] = None,
    ) -> None:
        return await super().create_relationships(fga_client, user_id, role, user_id)

    @classmethod
    async def delete_relationships(
        cls,
        fga_client: OpenFgaClient,
        user_id: int,
        role: LiteralString,
        object_id: Optional[int] = None,
    ) -> None:
        return await super().delete_relationships(fga_client, user_id, role, user_id)
