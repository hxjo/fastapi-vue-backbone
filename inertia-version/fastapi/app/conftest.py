from typing import Any, TypeVar
from unittest.mock import MagicMock

import pytest
from fastapi import BackgroundTasks
from httpx import AsyncClient
from openfga_sdk import ClientConfiguration, OpenFgaClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.deps.authz import get_fga_client
from app.common.deps.db import get_db
from app.common.deps.search import StructuredSearchClient, get_search_clients
from app.common.deps.tasks import tasks
from app.common.test_utils.authz import (
    create_store_and_authorization_model,
    delete_store,
)
from app.common.test_utils.db_utils import (
    async_create_database,
    async_database_exists,
    async_drop_database,
)
from app.common.test_utils.factory import Factory
from app.common.test_utils.search import (
    delete_search_indexes,
    get_test_search_clients,
)
from app.core.config import settings
from app.main import app as main_app

TEST_DATABASE_URL = settings.TEST_SQLALCHEMY_DATABASE_URI.unicode_string()  # type: ignore

# pylint: disable=redefined-outer-name; we are using fixtures


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db(worker_id):
    db_url = TEST_DATABASE_URL + f"_{worker_id}"
    if await async_database_exists(db_url):
        await async_drop_database(db_url)
    await async_create_database(db_url)
    engine = create_async_engine(db_url, echo=settings.DEBUG_SQL)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    await engine.dispose()

    yield

    await async_drop_database(db_url)


@pytest.fixture
async def engine(worker_id):
    db_url = TEST_DATABASE_URL + f"_{worker_id}"
    engine = create_async_engine(db_url, echo=settings.DEBUG_SQL)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def session(engine: AsyncEngine):
    connection = await engine.connect()
    transaction = await connection.begin()
    async with AsyncSession(bind=connection) as session_:
        yield session_
        await session_.rollback()
        await session_.close()

    if transaction.is_active:
        await transaction.rollback()
    await connection.close()


@pytest.fixture(autouse=True)
def background_tasks():
    return MagicMock(autospec=BackgroundTasks)


@pytest.fixture(scope="function")
async def fga_client(worker_id):
    store_id, authorization_model_id = await create_store_and_authorization_model(
        worker_id
    )
    async with OpenFgaClient(
        ClientConfiguration(
            api_scheme=settings.FGA_API_SCHEME,
            api_host=f"{settings.FGA_API_HOST}:{settings.FGA_API_PORT}",
            store_id=store_id,
            authorization_model_id=authorization_model_id,
        )
    ) as fga:
        try:
            yield fga
        finally:
            await fga.close()
            await delete_store(store_id)


@pytest.fixture(scope="function")
def search_clients(worker_id):
    clients = get_test_search_clients(worker_id)
    yield clients
    delete_search_indexes(worker_id)


@pytest.fixture(scope="function")
async def client(
    session: AsyncSession,
    background_tasks: BackgroundTasks,
    fga_client: OpenFgaClient,
    search_clients: StructuredSearchClient,
):
    async with AsyncClient(app=main_app, base_url="http://testserver") as client_:
        main_app.dependency_overrides[get_db] = lambda: session
        main_app.dependency_overrides[tasks] = lambda: background_tasks
        main_app.dependency_overrides[get_fga_client] = lambda: fga_client
        main_app.dependency_overrides[get_search_clients] = lambda: search_clients

        yield client_
        main_app.dependency_overrides.clear()


ModelT = TypeVar("ModelT", bound=Any)


@pytest.fixture
def factory(session, fga_client, search_clients):
    async def create_instance(model: ModelT, **kwargs) -> ModelT:
        return await Factory.create(
            session=session,
            fga_client=fga_client,
            search_clients=search_clients,
            model=model,
            **kwargs,
        )

    return create_instance
