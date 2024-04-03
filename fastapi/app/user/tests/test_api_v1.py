import unittest.mock

import pytest

from app.auth.utils.auth import verify_password_against_hash
from app.common.exceptions import NotFoundException
from app.common.test_utils.utils import authenticate_client, get_route
from app.user.api_v1 import (
    create_user,
    delete_user,
    get_user_by_id,
    get_user_me,
    search_users,
    update_user,
)
from app.user.fga import UserFGA
from app.user.models import User
from app.user.repository import UserRepo


class TestUserRoutes:
    async def test_create_user_endpoint(self, client):
        payload = {
            "email": "test@test.com",
            "username": "test",
            "password": "strong@Sass139",
        }
        response = await client.post(get_route(create_user), json=payload)
        assert response.status_code == 201
        content = response.json()
        assert content.get("email") == payload.get("email")
        assert content.get("username") == payload.get("username")
        assert content.get("is_active") is True
        assert content.get("password", None) is None

    async def test_get_user_by_id_endpoint(self, client, factory):
        user = await factory(User)
        authenticate_client(client, user.email)
        response = await client.get(get_route(get_user_by_id, user_id=user.id))
        assert response.status_code == 200

        content = response.json()
        assert content.get("email") == user.email
        assert content.get("username") == user.username
        assert content.get("is_active") == user.is_active
        assert content.get("password", None) is None

    async def test_patch_user_endpoint(self, client, factory, session):
        user = await factory(User)
        authenticate_client(client, user.email)
        new_password = "ABTest456!"
        payload = {
            "password": new_password,
        }

        response = await client.patch(
            get_route(update_user, user_id=user.id), json=payload
        )
        assert response.status_code == 201

        content = response.json()
        assert content.get("email") == user.email
        assert content.get("username") == user.username
        assert content.get("is_active") == user.is_active
        assert content.get("password", None) is None
        user_from_db = await UserRepo.get(session=session, id_=user.id)
        assert verify_password_against_hash(new_password, user_from_db.hashed_password)

    async def test_delete_user_endpoint(self, session, factory, client):
        user = await factory(User)
        authenticate_client(client, user.email)

        response = await client.delete(get_route(delete_user, user_id=user.id))
        assert response.status_code == 204

        with pytest.raises(NotFoundException):
            await UserRepo.get(session=session, id_=user.id)

    async def test_get_me_endpoint(self, factory, client):
        user = await factory(User)
        authenticate_client(client, user.email)
        response = await client.get(get_route(get_user_me))
        assert response.status_code == 200
        content = response.json()
        assert content["email"] == user.email
        assert content["username"] == user.username

    async def test_get_returns_my_restaurant_ids(self, factory, client):
        user = await factory(User)
        authenticate_client(client, user.email)
        response = await client.get(get_route(get_user_me))
        assert response.status_code == 200
        content = response.json()
        assert content["email"] == user.email
        assert content["username"] == user.username

    async def test_search_users_does_not_return_self(self, factory, client):
        for _ in range(10):
            await factory(User)

        client_user = await factory(User)
        authenticate_client(client, client_user.email)
        response = await client.get(get_route(search_users))
        assert response.status_code == 200
        content = response.json()
        assert len(content) == 10


class TestUserRouteErrors:
    async def test_cannot_get_non_existent_user(self, client, factory):
        user = await factory(User)
        authenticate_client(client, user.email)
        response = await client.get(get_route(get_user_by_id, user_id=user.id + 1))
        assert response.status_code == 403  # Relation does not exist

    async def test_cannot_create_user_with_same_email(self, client, factory):
        user = await factory(User)
        password = "SecurePassword132@"
        authenticate_client(client, user.email)

        payload = {
            "username": user.username,
            "email": user.email,
            "password": password,
        }

        response = await client.post(get_route(create_user), json=payload)

        assert response.status_code == 409

    async def test_cannot_create_user_with_unsecure_password(self, client):
        # Most of the tests are in the service (app.services.user.tests.test_password), we're only
        # testing the response here
        payload = {
            "username": "username",
            "email": "u@gmail.com",
            "password": "test",
        }

        response = await client.post(get_route(create_user), json=payload)
        assert response.status_code == 400

    async def test_cannot_patch_user_with_unsecure_password(self, client, factory):
        user = await factory(User)
        authenticate_client(client, user.email)
        payload = {
            "password": "test",
        }

        response = await client.patch(
            get_route(update_user, user_id=user.id), json=payload
        )
        assert response.status_code == 400

    async def test_cannot_create_user_with_invalid_email(self, client):
        payload = {
            "username": "username",
            "email": "test",
            "password": "strongPassWor15@",
        }

        response = await client.post(get_route(create_user), json=payload)
        assert response.status_code == 422

    async def test_cannot_patch_other_user(self, client, factory):
        user = await factory(User)
        authenticate_client(client, user.email)

        target_user_password = "Test123@"
        target_user = await factory(User, password=target_user_password)
        payload = {
            "email": target_user.email,
            "username": target_user.username,
            "password": target_user_password,
        }

        response = await client.patch(
            get_route(update_user, user_id=target_user.id), json=payload
        )
        assert response.status_code == 403

    async def test_cannot_delete_other_user(self, client, factory):
        user = await factory(User)
        authenticate_client(client, user.email)

        target_user = await factory(User)
        response = await client.delete(get_route(delete_user, user_id=target_user.id))
        assert response.status_code == 403

    async def test_cannot_set_itself_superuser_through_post(self, client, session):
        payload = {
            "username": "username",
            "email": "test@gmail.com",
            "password": "strongPassWor15@",
            "is_superuser": True,
        }

        response = await client.post(get_route(create_user), json=payload)
        assert response.status_code == 201
        content = response.json()
        db_user = await UserRepo.get(session, id_=content["id"])
        assert db_user.is_superuser is False

    async def test_cannot_set_itself_superuser_through_patch(self, client, factory):
        user = await factory(User)
        authenticate_client(client, user.email)
        payload = {
            "is_superuser": True,
        }

        response = await client.patch(
            get_route(update_user, user_id=user.id), json=payload
        )
        assert response.status_code == 201
        assert user.is_superuser is False


class TestUserRouteBackgroundTasks:
    async def test_user_create_triggers_tuple_creation(
        self, client, background_tasks, search_clients, session
    ):
        payload = {
            "username": "new_username",
            "email": "user@gmail.com",
            "password": "StrongPassw0rd!",
        }
        response = await client.post(get_route(create_user), json=payload)
        assert response.status_code == 201
        content = response.json()
        user_id = content.get("id")
        background_tasks.add_task.assert_any_call(
            UserFGA.create_relationships, unittest.mock.ANY, user_id, "client"
        )
        db_user = await UserRepo.get(session, id_=user_id)
        background_tasks.add_task.assert_any_call(
            search_clients.user.add_documents, [db_user]
        )

    async def test_user_delete_triggers_tuple_deletion(
        self, client, factory, background_tasks, search_clients
    ):
        user = await factory(User)
        authenticate_client(client, user.email)
        response = await client.delete(get_route(delete_user, user_id=user.id))
        assert response.status_code == 204
        background_tasks.add_task.assert_any_call(
            UserFGA.delete_relationships, unittest.mock.ANY, user.id, "client"
        )
        background_tasks.add_task.assert_any_call(
            search_clients.user.delete_document, user
        )

    async def test_user_update_triggers_index_update(
        self, client, factory, background_tasks, search_clients
    ):
        user = await factory(User)
        authenticate_client(client, user.email)
        response = await client.patch(
            get_route(update_user, user_id=user.id), json={"username": "new username"}
        )
        assert response.status_code == 201
        background_tasks.add_task.assert_any_call(
            search_clients.user.update_documents, [user]
        )


class TestUserRoutePermissions:
    async def test_cannot_read_user_without_authentication(self, factory, client):
        user = await factory(User)
        response = await client.get(get_route(get_user_by_id, user_id=user.id))
        assert response.status_code == 401

    async def test_cannot_patch_other_user(self, factory, client):
        user = await factory(User)
        user_email = user.email
        target_user = await factory(User)
        authenticate_client(client, user_email)
        response = await client.patch(
            get_route(update_user, user_id=target_user.id),
            json={"username": "new username"},
        )
        assert response.status_code == 403

    async def test_cannot_delete_other_user(self, factory, client):
        user = await factory(User)
        user_email = user.email
        target_user = await factory(User)
        authenticate_client(client, user_email)
        response = await client.delete(
            get_route(delete_user, user_id=target_user.id),
        )
        assert response.status_code == 403

    async def test_cannot_search_users_without_being_authenticated(self, client):
        response = await client.get(get_route(search_users))
        assert response.status_code == 401
