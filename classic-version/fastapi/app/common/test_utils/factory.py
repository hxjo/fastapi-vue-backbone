from typing import Any, TypeVar

from openfga_sdk import OpenFgaClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.models import AdminToken
from app.auth.tests.factory import new_default_admin_token
from app.common.deps.search import StructuredSearchClient
from app.user.models import User
from app.user.tests.factory import new_default_user

ModelT = TypeVar("ModelT", bound=Any)


class Factory:
    tuple_models_methods = [(User, "create_user"), (AdminToken, "create_admin_token")]

    @classmethod
    def get_method_for_model(cls, model: ModelT):
        for model_, method in cls.tuple_models_methods:
            if model == model_:
                return getattr(cls, method)
        raise ValueError(f"Model {model} not found in factory")

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        fga_client: OpenFgaClient,
        search_clients: StructuredSearchClient,
        model: ModelT,
        **kwargs,
    ) -> ModelT:
        return await cls.get_method_for_model(model)(
            session, fga_client, search_clients, **kwargs
        )

    @classmethod
    async def create_user(cls, session, fga_client, search_clients, **kwargs):
        return await new_default_user(session, fga_client, search_clients, **kwargs)

    @classmethod
    async def create_admin_token(cls, session, fga_client, search_clients, **kwargs):
        return await new_default_admin_token(
            session, fga_client, search_clients, **kwargs
        )
