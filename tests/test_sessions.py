import pytest


# REFRESH TOKEN - SUCCESS
@pytest.mark.asyncio
async def test_refresh_token(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_session_user",
            "email": "pytest_session@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_session@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

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


# REFRESH TOKEN - INVALID TOKEN
@pytest.mark.asyncio
async def test_refresh_token_invalid(client):

    response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": "invalid_refresh_token"
        }
    )

    assert response.status_code == 401


# REFRESH TOKEN - MISSING TOKEN
@pytest.mark.asyncio
async def test_refresh_token_missing(client):

    response = await client.post(
        "/api/v1/auth/refresh",
        json={}
    )

    assert response.status_code == 422


# LOGOUT - SUCCESS
@pytest.mark.asyncio
async def test_logout(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_logout_user",
            "email": "pytest_logout@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_logout@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    response = await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Logout successful"


# LOGOUT - INVALID TOKEN
@pytest.mark.asyncio
async def test_logout_invalid_token(client):

    response = await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": "invalid_refresh_token"
        }
    )

    assert response.status_code == 401


# LOGOUT - MISSING TOKEN
@pytest.mark.asyncio
async def test_logout_missing_token(client):

    response = await client.post(
        "/api/v1/auth/logout",
        json={}
    )

    assert response.status_code == 422


# REFRESH TOKEN AFTER LOGOUT
@pytest.mark.asyncio
async def test_refresh_after_logout(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_refresh_logout",
            "email": "pytest_refresh_logout@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_refresh_logout@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    logout_response = await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token
        }
    )

    assert logout_response.status_code == 200

    refresh_response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    assert refresh_response.status_code == 401