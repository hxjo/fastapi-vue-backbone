import json
import os
from typing import Optional, Tuple

from openfga_sdk import ClientConfiguration, OpenFgaClient
from openfga_sdk.models.create_store_request import CreateStoreRequest

from app.core.config import settings

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
JSON_AUTHZ_MODEL = os.path.join(
    ABSOLUTE_PATH, "..", "..", "..", "authorization", "model.json"
)


async def get_client_configuration(
    store_id: Optional[str] = None,
) -> ClientConfiguration:
    return ClientConfiguration(
        api_scheme=settings.FGA_API_SCHEME,
        api_host=f"{settings.FGA_API_HOST}:{settings.FGA_API_PORT}",
        store_id=store_id,
    )


async def create_store_and_authorization_model(worker_id: int) -> Tuple[str, str]:
    with open(JSON_AUTHZ_MODEL, "r", encoding="utf-8") as model:
        model_json = json.load(model)
        async with OpenFgaClient(
            ClientConfiguration(
                api_scheme=settings.FGA_API_SCHEME,
                api_host=f"{settings.FGA_API_HOST}:{settings.FGA_API_PORT}",
            )
        ) as client:
            response = await client.create_store(
                CreateStoreRequest(name=f"test_skeleton_{worker_id}")
            )
            store_id = response.id
            client.set_store_id(store_id)
            response = await client.write_authorization_model(model_json)
            authorization_id = response.authorization_model_id
            await client.close()
        return store_id, authorization_id


async def delete_store(store_id: str) -> None:
    async with OpenFgaClient(await get_client_configuration(store_id)) as client:
        await client.delete_store()
        await client.close()
