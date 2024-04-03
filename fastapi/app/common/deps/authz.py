from typing import Annotated, AsyncGenerator

from fastapi import Depends
from openfga_sdk import ClientConfiguration, OpenFgaClient

from app.core.config import settings

fga_client_configuration = ClientConfiguration(
    api_scheme=settings.FGA_API_SCHEME,
    api_host=f"{settings.FGA_API_HOST}:{settings.FGA_API_PORT}",
    store_id=settings.FGA_STORE_ID,
    authorization_model_id=settings.FGA_MODEL_ID,
)


async def get_fga_client() -> AsyncGenerator[OpenFgaClient, None]:
    async with OpenFgaClient(fga_client_configuration) as client:
        yield client

        await client.close()


FGAClientDep = Depends(get_fga_client)
AnnotatedFGAClientDep = Annotated[OpenFgaClient, FGAClientDep]
