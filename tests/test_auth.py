import pytest


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_register_user",
            "email": "pytest_register@example.com",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "User registered successfully"
    assert data["user"]["username"] == "pytest_register_user"
    assert data["user"]["email"] == "pytest_register@example.com"
    assert data["user"]["id"]


@pytest.mark.asyncio
async def test_login(client):
    # Register user first
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_login_user",
            "email": "pytest_login@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_login@example.com",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login successful"
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"

    assert data["user"]["username"] == "pytest_login_user"
    assert data["user"]["email"] == "pytest_login@example.com"


@pytest.mark.asyncio
async def test_login_invalid_password(client):
    # Register user first
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_invalid_login",
            "email": "pytest_invalid@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    # Login with wrong password
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_invalid@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"


@pytest.mark.asyncio
async def test_register_duplicate_username(client):
    # First registration
    first_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_duplicate_user",
            "email": "pytest_duplicate1@example.com",
            "password": "Test@12345"
        }
    )

    assert first_response.status_code == 201

    # Second registration with same username
    second_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_duplicate_user",
            "email": "pytest_duplicate2@example.com",
            "password": "Test@12345"
        }
    )

    assert second_response.status_code == 400

    data = second_response.json()

    assert data["detail"] == "Username already exists"

@pytest.mark.asyncio
async def test_refresh_token(client):

    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_refresh_user",
            "email": "pytest_refresh@example.com",
            "password": "Test@12345"
        }
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_refresh@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    refresh_token = login_data["refresh_token"]

    response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Access token refreshed successfully"
    assert data["access_token"]
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_invalid_refresh_token(client):

    response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": "invalid-refresh-token"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid or expired Refresh token"

@pytest.mark.asyncio
async def test_logout(client):

    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_logout_user",
            "email": "pytest_logout@example.com",
            "password": "Test@12345"
        }
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_logout@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    refresh_token = login_data["refresh_token"]

    response = await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Logout successful"


@pytest.mark.asyncio
async def test_get_current_user(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_me_user",
            "email": "pytest_me@example.com",
            "password": "Test@12345"
        }
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_me@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()
    access_token = login_data["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "pytest_me_user"
    assert data["email"] == "pytest_me@example.com"
    assert data["id"]


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client):
    response = await client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_rate_limit(client):

    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "rate_limit_user",
            "email": "rate_limit@example.com",
            "password": "Test@12345"
        }
    )

    for _ in range(5):
        await client.post(
            "/api/v1/auth/login",
            json={
                "email": "rate_limit@example.com",
                "password": "Test@12345"
            }
        )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "rate_limit@example.com",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 429

@pytest.mark.asyncio
async def test_register_rate_limit(client):

    for i in range(5):
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": f"rate_user_{i}",
                "email": f"rate_user_{i}@example.com",
                "password": "Test@12345"
            }
        )

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "rate_user_6",
            "email": "rate_user_6@example.com",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 429