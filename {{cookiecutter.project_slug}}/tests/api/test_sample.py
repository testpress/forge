from asgiref.sync import sync_to_async

from app.api.security import create_access_token
from tests.base import BaseAPITestCase
from tests.mixins.sample import UserMixin


class TestHealthAPI(BaseAPITestCase):
    async def test_health_needs_no_credentials(self):
        response = await self.async_client.get("/v1/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    async def test_ping(self):
        response = await self.async_client.get("/v1/ping")

        assert response.status_code == 200
        assert response.json() == {"message": "pong"}


class TestAuthAPI(BaseAPITestCase, UserMixin):
    async def test_login_returns_a_bearer_token(self):
        user = await sync_to_async(self.create_user)(password="s3cret-pass")

        response = await self.async_client.post(
            "/v1/auth/login",
            json={"phone_number": user.phone_number, "password": "s3cret-pass"},
        )

        assert response.status_code == 200
        assert response.json()["token_type"] == "bearer"
        assert response.json()["access_token"]

    async def test_login_rejects_a_wrong_password(self):
        user = await sync_to_async(self.create_user)(password="s3cret-pass")

        response = await self.async_client.post(
            "/v1/auth/login",
            json={"phone_number": user.phone_number, "password": "wrong"},
        )

        assert response.status_code == 401

    async def test_login_rejects_an_inactive_user(self):
        user = await sync_to_async(self.create_user)(
            password="s3cret-pass",
            is_active=False,
        )

        response = await self.async_client.post(
            "/v1/auth/login",
            json={"phone_number": user.phone_number, "password": "s3cret-pass"},
        )

        assert response.status_code == 401

    async def test_me_returns_the_token_owner(self):
        user = await sync_to_async(self.create_user)()
        token = create_access_token(user)

        response = await self.async_client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["phone_number"] == user.phone_number


class TestUsersAPI(BaseAPITestCase, UserMixin):
    async def test_listing_users_requires_authentication(self):
        response = await self.async_client.get("/v1/users/")

        assert response.status_code == 401

    async def test_a_garbage_token_is_rejected(self):
        response = await self.async_client.get(
            "/v1/users/",
            headers={"Authorization": "Bearer not-a-real-token"},
        )

        assert response.status_code == 401

    async def test_list_users_is_paginated(self):
        user = await sync_to_async(self.create_user)()

        response = await self.async_client.get(
            "/v1/users/",
            headers={"Authorization": f"Bearer {create_access_token(user)}"},
        )

        assert response.status_code == 200
        assert response.json()["count"] == 1
        assert response.json()["items"][0]["id"] == user.pk

    async def test_get_unknown_user_is_404(self):
        user = await sync_to_async(self.create_user)()

        response = await self.async_client.get(
            "/v1/users/99999",
            headers={"Authorization": f"Bearer {create_access_token(user)}"},
        )

        assert response.status_code == 404

    async def test_create_user_hashes_the_password(self):
        user = await sync_to_async(self.create_user)()

        response = await self.async_client.post(
            "/v1/users/",
            json={"phone_number": "+15550009999", "password": "another-pass"},
            headers={"Authorization": f"Bearer {create_access_token(user)}"},
        )

        assert response.status_code == 201

        created = await sync_to_async(self.get_user)(response.json()["id"])
        assert created.password != "another-pass"
        assert created.check_password("another-pass")

    async def test_create_user_rejects_a_duplicate_phone_number(self):
        user = await sync_to_async(self.create_user)()

        response = await self.async_client.post(
            "/v1/users/",
            json={"phone_number": user.phone_number, "password": "another-pass"},
            headers={"Authorization": f"Bearer {create_access_token(user)}"},
        )

        assert response.status_code == 409

    async def test_create_user_rejects_a_malformed_email(self):
        user = await sync_to_async(self.create_user)()

        response = await self.async_client.post(
            "/v1/users/",
            json={
                "phone_number": "+15550008888",
                "password": "another-pass",
                "email": "not-an-email",
            },
            headers={"Authorization": f"Bearer {create_access_token(user)}"},
        )

        assert response.status_code == 422

    async def test_patch_only_touches_the_fields_sent(self):
        user = await sync_to_async(self.create_user)(email="before@example.com")

        response = await self.async_client.patch(
            f"/v1/users/{user.pk}",
            json={"email": "after@example.com"},
            headers={"Authorization": f"Bearer {create_access_token(user)}"},
        )

        assert response.status_code == 200
        assert response.json()["email"] == "after@example.com"
        assert response.json()["phone_number"] == user.phone_number

    async def test_delete_user(self):
        user = await sync_to_async(self.create_user)()
        target = await sync_to_async(self.create_user)()

        response = await self.async_client.delete(
            f"/v1/users/{target.pk}",
            headers={"Authorization": f"Bearer {create_access_token(user)}"},
        )

        assert response.status_code == 204
