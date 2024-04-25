import logging
from typing import List, Literal, LiteralString, cast

from openfga_sdk import OpenFgaClient
from openfga_sdk.client.models.check_request import ClientCheckRequest
from openfga_sdk.client.models.tuple import ClientTuple
from openfga_sdk.client.models.write_request import ClientWriteRequest

AllowedUserRelations = Literal["can_read", "can_update", "can_delete"]

UserRole = Literal["superuser", "user"]

logger = logging.getLogger(__name__)


class BaseFGA:
    object_name: str

    @classmethod
    def has_user_relationship(
        cls, user_id: int, relationship: str, target_object_id: int
    ) -> ClientCheckRequest:
        logger.info(
            f"Checking relationship {relationship} between initiator {user_id} and object {target_object_id}"
        )
        return ClientCheckRequest(
            user=f"user:{user_id}",
            relation=relationship,
            object=f"{cls.object_name}:{target_object_id}",
        )

    @staticmethod
    def get_tuples(user_id: int, role: str, object_id: int) -> List[ClientTuple]:
        raise NotImplementedError()

    @classmethod
    async def create_relationships(
        cls,
        fga_client: OpenFgaClient,
        user_id: int,
        role: LiteralString,
        object_id: int,
    ) -> None:
        logger.info(
            f"Creating relationship {role} between initiator {user_id} and object {object_id}"
        )
        body = ClientWriteRequest(
            writes=cls.get_tuples(user_id, role, object_id),
        )
        await fga_client.write(body)

    @classmethod
    async def delete_relationships(
        cls,
        fga_client: OpenFgaClient,
        user_id: int,
        role: LiteralString,
        object_id: int,
    ) -> None:
        logger.info(
            f"Deleting relationship {role} between initiator {user_id} and object {object_id}"
        )
        body = ClientWriteRequest(deletes=cls.get_tuples(user_id, role, object_id))
        await fga_client.write(body)

    @staticmethod
    async def check(fga_client: OpenFgaClient, body: ClientCheckRequest) -> bool:
        response = await fga_client.check(body)
        return cast(bool, response.allowed)

    @classmethod
    async def can_read(
        cls, fga_client: OpenFgaClient, user_id: int, object_id: int
    ) -> bool:
        body = cls.has_user_relationship(user_id, "can_read", object_id)
        return await cls.check(fga_client, body)

    @classmethod
    async def can_update(
        cls, fga_client: OpenFgaClient, user_id: int, object_id: int
    ) -> bool:
        body = cls.has_user_relationship(user_id, "can_update", object_id)
        return await cls.check(fga_client, body)

    @classmethod
    async def can_delete(
        cls, fga_client: OpenFgaClient, user_id: int, object_id: int
    ) -> bool:
        body = cls.has_user_relationship(user_id, "can_delete", object_id)
        return await cls.check(fga_client, body)
