import pytest
from httpx import AsyncClient
from jose import jwt
from datetime import datetime, timedelta, timezone

# Настройки для тестов
BASE_URL = "http://localhost:8001/auth"  # URL микросервиса
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Тестовые данные
TEST_USER = {
    "username": "testuser7",
    "password": "testpassword7"
}

# Тестовые данные
TEST_USER2 = {
    "username": "testuser1",
    "password": "testpassword1"
}


@pytest.mark.asyncio
async def test_register():
    async with AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/register", params=TEST_USER2)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["username"] == TEST_USER2["username"]
        #assert "balance" in data


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient() as client:
        # Авторизация
        response = await client.post(f"{BASE_URL}/login", params=TEST_USER)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

        # Проверка токена
        payload = jwt.decode(data["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
        assert payload.get("sub") is not None
        assert isinstance(payload["sub"], str)


@pytest.mark.asyncio
async def test_verify_token():
    # Создание тестового токена
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    test_token = jwt.encode({"sub": "1", "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(f"{BASE_URL}/verify-token", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == 1


@pytest.mark.asyncio
async def test_invalid_credentials():
    async with AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/login", params={"username": "wrong", "password": "wrong"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_invalid_token():
    async with AsyncClient() as client:
        headers = {"Authorization": "Bearer invalid_token"}
        response = await client.post(f"{BASE_URL}/verify-token", headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token payload"
