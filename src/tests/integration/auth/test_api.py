from unittest.mock import patch

import pytest
from httpx import AsyncClient

from src.core.cache.cache_manager import Cache
from src.core.error.codes import INVALID_CRED, INVALID_USER
from src.core.error.format_error import ERROR_MAPPER


@pytest.mark.asyncio(loop_scope="session")
class TestAuthAPI:

    async def test_registration_success(self, test_client: AsyncClient) -> None:
        registration_data = {
            "phone": "01630811627",
            "email": "mahmudul.hassan240@gmail.com",
            "name": "Mahmudul Hassan",
            "dob": "1994-04-07",
            "gender": "MALE",
            "password": "123456",
        }

        with patch.object(Cache, "set"), patch.object(
            Cache, "get", return_value="555555"
        ):
            response = await test_client.post(
                "/api/v1/auth/register/", json=registration_data
            )
        result = response.json()
        assert response.status_code == 200
        assert "access_token" in result["data"]
        assert "refresh_token" in result["data"]

    async def test_login_success(self, test_client: AsyncClient) -> None:
        login_data = {
            "email": "mahmudul.hassan240@gmail.com",
            "password": "123456",
        }
        with patch.object(Cache, "set"):
            response = await test_client.post("/api/v1/auth/login/", json=login_data)
        result = response.json()
        assert response.status_code == 200
        assert "access_token" in result["data"]
        assert "refresh_token" in result["data"]

    async def test_login_failed(self, test_client: AsyncClient) -> None:
        login_data = {
            "email": "mahmudul.hassan240@gmail.com",
            "password": "1234567",
        }
        with patch.object(Cache, "set"):
            response = await test_client.post("/api/v1/auth/login/", json=login_data)

        result = response.json()
        assert ERROR_MAPPER[INVALID_CRED] == result["error"]
        assert response.status_code == 400
