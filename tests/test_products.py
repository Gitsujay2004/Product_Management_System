import pytest


# ============================================================
# GET ALL PRODUCTS - AUTHENTICATED USER
# ============================================================

@pytest.mark.asyncio
async def test_get_products_authenticated(client):

    # Register user
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_product_user",
            "email": "pytest_product@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201


    # Login
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_product@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]


    # Get products
    response = await client.get(
        "/api/v1/products/",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert "pagination" in data


# ============================================================
# GET ALL PRODUCTS - WITHOUT TOKEN
# ============================================================

@pytest.mark.asyncio
async def test_get_products_without_token(client):

    response = await client.get(
        "/api/v1/products/"
    )

    assert response.status_code == 401


# ============================================================
# GET PRODUCT BY ID
# ============================================================

@pytest.mark.asyncio
async def test_get_product_by_id(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]


    # --------------------------------------------------------
    # Create Category
    # --------------------------------------------------------

    category_response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_product_category"
        },
        headers=headers
    )

    assert category_response.status_code == 201

    category_data = category_response.json()

    category_id = category_data["data"]["id"]


    # --------------------------------------------------------
    # Create Product
    # --------------------------------------------------------

    product_response = await client.post(
        "/api/v1/products/",
        json={
            "name": "pytest_get_product",
            "price": 999.99,
            "stock": 10,
            "status": "active",
            "description": "Test product for GET by ID",
            "sku": "PYTEST-GET-001",
            "category_id": category_id,
            "images": []
        },
        headers=headers
    )

    assert product_response.status_code == 201

    product_data = product_response.json()

    product_id = product_data["data"]["id"]


    # --------------------------------------------------------
    # Get Product By ID
    # --------------------------------------------------------

    response = await client.get(
        f"/api/v1/products/{product_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["id"] == product_id
    assert data["data"]["name"] == "pytest_get_product"
    assert data["data"]["sku"] == "PYTEST-GET-001"


# ============================================================
# GET PRODUCT - NOT FOUND
# ============================================================

@pytest.mark.asyncio
async def test_get_product_not_found(client):

    # Register user
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_product_not_found",
            "email": "pytest_product_not_found@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201


    # Login
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_product_not_found@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]


    # Get non-existing product
    response = await client.get(
        "/api/v1/products/00000000-0000-0000-0000-000000000000",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_product(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    category_response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_create_category"
        },
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["data"]["id"]

    response = await client.post(
        "/api/v1/products/",
        json={
            "name": "pytest_create_product",
            "price": 499.99,
            "stock": 20,
            "status": "active",
            "description": "Test product creation",
            "sku": "PYTEST-CREATE-001",
            "category_id": category_id,
            "images": []
        },
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Product created successfully"
    assert data["data"]["id"]
    assert data["data"]["name"] == "pytest_create_product"
    assert data["data"]["price"] == "499.99"
    assert data["data"]["stock"] == 20
    assert data["data"]["sku"] == "PYTEST-CREATE-001"


@pytest.mark.asyncio
async def test_create_product_without_admin(client):

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_product_normal",
            "email": "pytest_product_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_product_normal@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = await client.post(
        "/api/v1/products/",
        json={
            "name": "pytest_non_admin_product",
            "price": 100.00,
            "stock": 10,
            "status": "active",
            "description": "Normal user product test",
            "sku": "PYTEST-NORMAL-001",
            "category_id": "00000000-0000-0000-0000-000000000000",
            "images": []
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_product_validation_error(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.post(
        "/api/v1/products/",
        json={
            "name": "",
            "price": -100,
            "stock": -5,
            "status": "",
            "description": "abc",
            "sku": "",
            "category_id": "00000000-0000-0000-0000-000000000000",
            "images": []
        },
        headers=headers
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error_code"] == "VALIDATION_ERROR"

@pytest.mark.asyncio
async def test_update_product(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    category_response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_update_category"
        },
        headers=headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["data"]["id"]

    create_response = await client.post(
        "/api/v1/products/",
        json={
            "name": "pytest_update_product",
            "price": 500.00,
            "stock": 10,
            "status": "active",
            "description": "Product before update",
            "sku": "PYTEST-UPDATE-001",
            "category_id": category_id,
            "images": []
        },
        headers=headers
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["data"]["id"]

    response = await client.put(
        f"/api/v1/products/{product_id}",
        json={
            "name": "pytest_updated_product",
            "price": 750.00,
            "stock": 25,
            "status": "active",
            "description": "Product after update",
            "sku": "PYTEST-UPDATED-001",
            "category_id": category_id
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["id"] == product_id
    assert data["data"]["name"] == "pytest_updated_product"
    assert data["data"]["price"] == "750.00"
    assert data["data"]["stock"] == 25
    assert data["data"]["sku"] == "PYTEST-UPDATED-001"

@pytest.mark.asyncio
async def test_update_product_without_admin(client):

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
        "/api/v1/products/00000000-0000-0000-0000-000000000000",
        json={
            "name": "pytest_updated_product",
            "price": 750.00,
            "stock": 25,
            "status": "active",
            "description": "Product update test",
            "sku": "PYTEST-UPDATED-001",
            "category_id": "00000000-0000-0000-0000-000000000000"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_product_not_found(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.put(
        "/api/v1/products/00000000-0000-0000-0000-000000000000",
        json={
            "name": "pytest_not_found_product",
            "price": 500.00,
            "stock": 10,
            "status": "active",
            "description": "Product not found test",
            "sku": "PYTEST-NOTFOUND-001",
            "category_id": "00000000-0000-0000-0000-000000000000"
        },
        headers=headers
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_product_validation_error(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.put(
        "/api/v1/products/00000000-0000-0000-0000-000000000000",
        json={
            "name": "",
            "price": -100,
            "stock": -5,
            "status": "",
            "description": "abc",
            "sku": "",
            "category_id": "00000000-0000-0000-0000-000000000000"
        },
        headers=headers
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error_code"] == "VALIDATION_ERROR"

@pytest.mark.asyncio
async def test_delete_product(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    category_response = await client.post(
        "/api/v1/categories/",
        json={
            "name": "pytest_delete_category"
        },
        headers=headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["data"]["id"]

    create_response = await client.post(
        "/api/v1/products/",
        json={
            "name": "pytest_delete_product",
            "price": 600.00,
            "stock": 15,
            "status": "active",
            "description": "Product for delete testing",
            "sku": "PYTEST-DELETE-001",
            "category_id": category_id,
            "images": []
        },
        headers=headers
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["data"]["id"]

    response = await client.delete(
        f"/api/v1/products/{product_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Product deleted successfully"

    # Verify product no longer exists
    get_response = await client.get(
        f"/api/v1/products/{product_id}",
        headers=headers
    )

    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_product_without_admin(client):

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
        "/api/v1/products/00000000-0000-0000-0000-000000000000",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_product_not_found(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.delete(
        "/api/v1/products/00000000-0000-0000-0000-000000000000",
        headers=headers
    )

    assert response.status_code == 404

