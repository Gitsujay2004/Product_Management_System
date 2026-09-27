import pytest


# ============================================================
# GET ALL CATEGORIES - AUTHENTICATED USER
# ============================================================

@pytest.mark.asyncio
async def test_get_categories_authenticated(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_category_user",
            "email": "pytest_category@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_category@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/categories/",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "categories fetched successfully"
    assert "data" in data


# ============================================================
# GET ALL CATEGORIES - WITHOUT TOKEN
# ============================================================

@pytest.mark.asyncio
async def test_get_categories_without_token(client):

    response = await client.get(
        "/api/v1/categories/"
    )

    assert response.status_code == 401


# ============================================================
# GET CATEGORY BY ID
# ============================================================

@pytest.mark.asyncio
async def test_get_category_by_id(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    create_response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_get_category"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    category_id = create_response.json()["data"]["id"]

    response = await client.get(
        f"/api/v1/categories/{category_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["id"] == category_id
    assert data["data"]["name"] == "pytest_get_category"


# ============================================================
# GET CATEGORY - NOT FOUND
# ============================================================

@pytest.mark.asyncio
async def test_get_category_not_found(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.get(
        "/api/v1/categories/00000000-0000-0000-0000-000000000000",
        headers=headers
    )

    assert response.status_code == 404


# ============================================================
# CREATE CATEGORY
# ============================================================

@pytest.mark.asyncio
async def test_create_category(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_create_category"
        },
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Category created successfully"
    assert data["data"]["id"]
    assert data["data"]["name"] == "pytest_create_category"


# ============================================================
# CREATE CATEGORY - WITHOUT ADMIN
# ============================================================

@pytest.mark.asyncio
async def test_create_category_without_admin(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_category_normal",
            "email": "pytest_category_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_category_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_non_admin_category"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403


# ============================================================
# CREATE DUPLICATE CATEGORY
# ============================================================

@pytest.mark.asyncio
async def test_create_duplicate_category(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    first_response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_duplicate_category"
        },
        headers=headers
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_duplicate_category"
        },
        headers=headers
    )

    assert second_response.status_code == 400

    data = second_response.json()

    assert data["detail"] == "Category already exists"


# ============================================================
# UPDATE CATEGORY
# ============================================================

@pytest.mark.asyncio
async def test_update_category(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    create_response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_update_category"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    category_id = create_response.json()["data"]["id"]

    response = await client.put(
        f"/api/v1/categories/{category_id}",
        json={
            "name": "pytest_updated_category"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["id"] == category_id
    assert data["data"]["name"] == "pytest_updated_category"


# ============================================================
# UPDATE CATEGORY - WITHOUT ADMIN
# ============================================================

@pytest.mark.asyncio
async def test_update_category_without_admin(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_category_update_normal",
            "email": "pytest_category_update_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_category_update_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = await client.put(
        "/api/v1/categories/00000000-0000-0000-0000-000000000000",
        json={
            "name": "pytest_updated_category"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403


# ============================================================
# UPDATE CATEGORY - NOT FOUND
# ============================================================

@pytest.mark.asyncio
async def test_update_category_not_found(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.put(
        "/api/v1/categories/00000000-0000-0000-0000-000000000000",
        json={
            "name": "pytest_not_found_category"
        },
        headers=headers
    )

    assert response.status_code == 404


# ============================================================
# DELETE CATEGORY
# ============================================================

@pytest.mark.asyncio
async def test_delete_category(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    create_response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_delete_category"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    category_id = create_response.json()["data"]["id"]

    response = await client.delete(
        f"/api/v1/categories/{category_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Category deleted successfully"

    get_response = await client.get(
        f"/api/v1/categories/{category_id}",
        headers=headers
    )

    assert get_response.status_code == 404


# ============================================================
# DELETE CATEGORY - WITHOUT ADMIN
# ============================================================

@pytest.mark.asyncio
async def test_delete_category_without_admin(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_category_delete_normal",
            "email": "pytest_category_delete_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_category_delete_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = await client.delete(
        "/api/v1/categories/00000000-0000-0000-0000-000000000000",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403


# ============================================================
# DELETE CATEGORY - CATEGORY IN USE
# ============================================================

@pytest.mark.asyncio
async def test_delete_category_in_use(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    # Create category
    category_response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_category_in_use"
        },
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["data"]["id"]

    # Create product using the category
    product_response = await client.post(
        "/api/v1/products/",
        json={
            "name": "pytest_category_in_use_product",
            "price": 500.00,
            "stock": 10,
            "status": "active",
            "description": "Product using category",
            "sku": "PYTEST-CATEGORY-USE-001",
            "category_id": category_id,
            "images": []
        },
        headers=headers
    )

    assert product_response.status_code == 201

    # Try to delete category
    response = await client.delete(
        f"/api/v1/categories/{category_id}",
        headers=headers
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == (
        "Cannot delete category because products are assigned to it"
    )