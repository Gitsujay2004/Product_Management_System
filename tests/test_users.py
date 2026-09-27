import pytest


# GET CURRENT USER
@pytest.mark.asyncio
async def test_get_current_user(admin_client):
    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.get(
        "/api/v1/users/me",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Profile fetched successfully"
    assert data["data"]["username"] == "pytest_admin"
    assert data["data"]["email"] == "pytest_admin@example.com"
    assert data["data"]["role"] == "admin"
    assert data["data"]["is_active"] is True

    
# GET CURRENT USER - WITHOUT TOKEN
@pytest.mark.asyncio
async def test_get_current_user_without_token(client):
    response = await client.get(
        "/api/v1/users/me"
    )

    assert response.status_code == 401


# GET USERS - ADMIN
@pytest.mark.asyncio
async def test_get_users(admin_client):
    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.get(
        "/api/v1/users/",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data


# GET USERS - WITHOUT ADMIN
@pytest.mark.asyncio
async def test_get_users_without_admin(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_normal_user",
            "email": "pytest_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/users/",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403


# GET USER BY ID
@pytest.mark.asyncio
async def test_get_user_by_id(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    create_response = await client.post(
        "/api/v1/users/",
        json={
            "username": "pytest_get_user",
            "email": "pytest_get_user@example.com",
            "password": "Test@12345"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["data"]["id"]

    response = await client.get(
        f"/api/v1/users/{user_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["id"] == user_id
    assert data["data"]["username"] == "pytest_get_user"
    assert data["data"]["email"] == "pytest_get_user@example.com"


# GET USER BY ID - NOT FOUND
@pytest.mark.asyncio
async def test_get_user_not_found(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.get(
        "/api/v1/users/00000000-0000-0000-0000-000000000000",
        headers=headers
    )

    assert response.status_code == 404


# CREATE USER
@pytest.mark.asyncio
async def test_create_user(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.post(
        "/api/v1/users/",
        json={
            "username": "pytest_create_user",
            "email": "pytest_create_user@example.com",
            "password": "Test@12345"
        },
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["data"]["id"]
    assert data["data"]["username"] == "pytest_create_user"
    assert data["data"]["email"] == "pytest_create_user@example.com"

    # Password should never be returned
    assert "password" not in data["data"]


# CREATE USER - WITHOUT ADMIN
@pytest.mark.asyncio
async def test_create_user_without_admin(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_create_normal",
            "email": "pytest_create_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_create_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = await client.post(
        "/api/v1/users/",
        json={
            "username": "pytest_not_admin_create",
            "email": "pytest_not_admin_create@example.com",
            "password": "Test@12345"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403


# CREATE USER - DUPLICATE USERNAME
@pytest.mark.asyncio
async def test_create_duplicate_username(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    first_response = await client.post(
        "/api/v1/users/",
        json={
            "username": "pytest_duplicate_username",
            "email": "pytest_duplicate_1@example.com",
            "password": "Test@12345"
        },
        headers=headers
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/api/v1/users/",
        json={
            "username": "pytest_duplicate_username",
            "email": "pytest_duplicate_2@example.com",
            "password": "Test@12345"
        },
        headers=headers
    )

    assert second_response.status_code == 400

    data = second_response.json()

    assert data["detail"] == "Username already exists"


# CREATE USER - DUPLICATE EMAIL
@pytest.mark.asyncio
async def test_create_duplicate_email(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    first_response = await client.post(
        "/api/v1/users/",
        json={
            "username": "pytest_duplicate_email_1",
            "email": "pytest_duplicate_email@example.com",
            "password": "Test@12345"
        },
        headers=headers
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/api/v1/users/",
        json={
            "username": "pytest_duplicate_email_2",
            "email": "pytest_duplicate_email@example.com",
            "password": "Test@12345"
        },
        headers=headers
    )

    assert second_response.status_code == 400

    data = second_response.json()

    assert data["detail"] == "Email already exists"


# UPDATE USER
@pytest.mark.asyncio
async def test_update_user(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    create_response = await client.post(
        "/api/v1/users/",
        json={
            "username": "pytest_update_user",
            "email": "pytest_update_user@example.com",
            "password": "Test@12345"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["data"]["id"]

    response = await client.put(
        f"/api/v1/users/{user_id}",
        json={
            "username": "pytest_updated_user",
            "email": "pytest_updated_user@example.com",
            "password": "NewTest@12345"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["id"] == user_id
    assert data["data"]["username"] == "pytest_updated_user"
    assert data["data"]["email"] == "pytest_updated_user@example.com"

    assert "password" not in data["data"]


# UPDATE USER - WITHOUT ADMIN
@pytest.mark.asyncio
async def test_update_user_without_admin(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_update_normal",
            "email": "pytest_update_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_update_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = await client.put(
        "/api/v1/users/00000000-0000-0000-0000-000000000000",
        json={
            "username": "pytest_updated_normal",
            "email": "pytest_updated_normal@example.com",
            "password": "Test@12345"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403


# UPDATE USER - NOT FOUND
@pytest.mark.asyncio
async def test_update_user_not_found(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.put(
        "/api/v1/users/00000000-0000-0000-0000-000000000000",
        json={
            "username": "pytest_not_found",
            "email": "pytest_not_found@example.com",
            "password": "Test@12345"
        },
        headers=headers
    )

    assert response.status_code == 404


# UPDATE USER STATUS
@pytest.mark.asyncio
async def test_update_user_status(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    create_response = await client.post(
        "/api/v1/users/",
        json={
            "username": "pytest_status_user",
            "email": "pytest_status@example.com",
            "password": "Test@12345"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["data"]["id"]

    response = await client.patch(
        f"/api/v1/users/{user_id}/status",
        json={
            "is_active": False
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["is_active"] is False


# DELETE USER
@pytest.mark.asyncio
async def test_delete_user(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    create_response = await client.post(
        "/api/v1/users/",
        json={
            "username": "pytest_delete_user",
            "email": "pytest_delete_user@example.com",
            "password": "Test@12345"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["data"]["id"]

    response = await client.delete(
        f"/api/v1/users/{user_id}",
        headers=headers
    )

    assert response.status_code == 200

    get_response = await client.get(
        f"/api/v1/users/{user_id}",
        headers=headers
    )

    assert get_response.status_code == 404


# DELETE USER - WITHOUT ADMIN
@pytest.mark.asyncio
async def test_delete_user_without_admin(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_delete_normal",
            "email": "pytest_delete_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_delete_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = await client.delete(
        "/api/v1/users/00000000-0000-0000-0000-000000000000",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403


# DELETE USER - NOT FOUND
@pytest.mark.asyncio
async def test_delete_user_not_found(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.delete(
        "/api/v1/users/00000000-0000-0000-0000-000000000000",
        headers=headers
    )

    assert response.status_code == 404