from app.auth.api import login
from app.auth.models import AdminToken
from app.auth.utils.auth import get_token_content
from app.common.test_utils.utils import authenticate_client, get_route
from app.user.api_v1 import get_user_by_id
from app.user.models import User


class TestLoginRoute:
    async def test_login_route_returns_valid_token(self, client, factory):
        password = "Test123@"
        user = await factory(User, password=password)
        payload = {
            "username": user.email,
            "password": password,
        }
        response = await client.post(get_route(login), data=payload)
        assert response.status_code == 200
        content = response.json()
        access_token = content.get("access_token", None)
        assert access_token is not None
        assert content.get("token_type", None) == "bearer"
        token_decoded = get_token_content(access_token)
        assert token_decoded.get("email") == user.email


class TestAuthDependency:
    async def test_get_with_expired_token_returns_401(self, client, factory):
        user = await factory(User)
        authenticate_client(client, user.email, expires_minutes=-1)
        user_id = user.id
        response = await client.get(get_route(get_user_by_id, user_id=user_id))
        assert response.status_code == 401

    async def test_get_with_admin_token_returns_401_when_user_is_not_superuser(
        self, client, factory
    ):
        user_ = await factory(User, is_superuser=False)
        user_id = user_.id
        token = await factory(AdminToken, user=user_)
        client.headers.update({"Authorization": f"Bearer {token.token}"})
        response = await client.get(get_route(get_user_by_id, user_id=user_id))
        assert response.status_code == 401

    async def test_get_with_admin_token_returns_200_when_user_is_superuser(
        self, client, factory
    ):
        user_ = await factory(User, is_superuser=True)
        user_id = user_.id
        token = await factory(AdminToken, user=user_)
        client.headers.update({"Authorization": f"Bearer {token.token}"})
        response = await client.get(get_route(get_user_by_id, user_id=user_id))
        assert response.status_code == 200
