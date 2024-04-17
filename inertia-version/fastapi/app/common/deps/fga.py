from typing import Annotated, AsyncGenerator
import os
from fastapi import Depends
from openfga_sdk import ClientConfiguration, OpenFgaClient

from app.core.config import settings

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
AUTHORIZATION_MODEL_ID_FILE = os.path.join(ABSOLUTE_PATH, '..', '..', '.fga_authorization_model_id')
STORE_ID_FILE = os.path.join(ABSOLUTE_PATH, '..', '..', '.fga_store_id')

def get_fga_config():
    if not os.path.isfile(AUTHORIZATION_MODEL_ID_FILE):
        with open(AUTHORIZATION_MODEL_ID_FILE, "w", encoding="utf-8") as file:
            file.write("")
    if not os.path.isfile(STORE_ID_FILE):
        with open(STORE_ID_FILE, "w", encoding="utf-8") as file:
            file.write("")

    authorization_model_id = open(AUTHORIZATION_MODEL_ID_FILE).read().strip()
    store_id = open(STORE_ID_FILE).read().strip()

    return ClientConfiguration(
        api_scheme=settings.FGA_API_SCHEME,
        api_host=f"{settings.FGA_API_HOST}:{settings.FGA_API_PORT}",
        store_id=store_id,
        authorization_model_id=authorization_model_id,
    )

async def get_fga_client() -> AsyncGenerator[OpenFgaClient, None]:
    config = get_fga_config()
    async with OpenFgaClient(config) as client:
        yield client

        await client.close()


FGAClientDep = Depends(get_fga_client)
AnnotatedFGAClientDep = Annotated[OpenFgaClient, FGAClientDep]
