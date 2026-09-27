import pytest


# CREATE PRODUCT IMAGE
@pytest.mark.asyncio
async def test_create_product_image(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    product_response = await client.post(
        "/api/v1/products/",
        json={
            "name": "pytest_image_product",
            "price": 500.00,
            "stock": 10,
            "status": "active",
            "description": "Product for image testing",
            "sku": "PYTEST-IMAGE-001",
            "category_id": (
                await client.post(
                    "/api/v1/categories/",
                    json={"name": "pytest_image_category"},
                    headers=headers
                )
            ).json()["data"]["id"],
            "images": []
        },
        headers=headers
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["data"]["id"]

    response = await client.post(
        "/api/v1/product-images/",
        json={
            "product_id": product_id,
            "url": "https://example.com/product.jpg",
            "is_primary": True
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "product image inserted successfully"


# GET ALL PRODUCT IMAGES
@pytest.mark.asyncio
async def test_get_product_images(client):

    response = await client.get(
        "/api/v1/product-images/"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "product images fetched successfully"
    assert "data" in data


# GET PRODUCT IMAGE BY ID
@pytest.mark.asyncio
async def test_get_product_image_by_id(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    category_response = await client.post(
        "/api/v1/categories/",
        json={"name": "pytest_image_get_category"},
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["data"]["id"]

    product_response = await client.post(
        "/api/v1/products/",
        json={
            "name": "pytest_image_get_product",
            "price": 600.00,
            "stock": 20,
            "status": "active",
            "description": "Product for image get testing",
            "sku": "PYTEST-IMAGE-GET-001",
            "category_id": category_id,
            "images": []
        },
        headers=headers
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["data"]["id"]

    create_response = await client.post(
        "/api/v1/product-images/",
        json={
            "product_id": product_id,
            "url": "https://example.com/get-image.jpg",
            "is_primary": True
        },
        headers=headers
    )

    assert create_response.status_code == 200

    # Get all images and find the created image
    images_response = await client.get(
        "/api/v1/product-images/"
    )

    assert images_response.status_code == 200

    images = images_response.json()["data"]

    image = next(
        image for image in images
        if image["product_id"] == product_id
    )

    image_id = image["id"]

    response = await client.get(
        f"/api/v1/product-images/{image_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "product image fetched successfully"
    assert data["data"]["id"] == image_id
    assert data["data"]["product_id"] == product_id
    assert data["data"]["url"] == "https://example.com/get-image.jpg"
    assert data["data"]["is_primary"] is True


# GET PRODUCT IMAGE - NOT FOUND
@pytest.mark.asyncio
async def test_get_product_image_not_found(client):

    response = await client.get(
        "/api/v1/product-images/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "product image not found"


# UPDATE PRODUCT IMAGE
@pytest.mark.asyncio
async def test_update_product_image(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    category_response = await client.post(
        "/api/v1/categories/",
        json={"name": "pytest_image_update_category"},
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["data"]["id"]

    product_response = await client.post(
        "/api/v1/products/",
        json={
            "name": "pytest_image_update_product",
            "price": 700.00,
            "stock": 15,
            "status": "active",
            "description": "Product for image update testing",
            "sku": "PYTEST-IMAGE-UPDATE-001",
            "category_id": category_id,
            "images": []
        },
        headers=headers
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["data"]["id"]

    create_response = await client.post(
        "/api/v1/product-images/",
        json={
            "product_id": product_id,
            "url": "https://example.com/old-image.jpg",
            "is_primary": False
        },
        headers=headers
    )

    assert create_response.status_code == 200

    images_response = await client.get(
        "/api/v1/product-images/"
    )

    images = images_response.json()["data"]

    image = next(
        image for image in images
        if image["product_id"] == product_id
    )

    image_id = image["id"]

    response = await client.put(
        f"/api/v1/product-images/{image_id}",
        json={
            "product_id": product_id,
            "url": "https://example.com/new-image.jpg",
            "is_primary": True
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "product image updated successfully"
    assert data["data"]["id"] == image_id
    assert data["data"]["url"] == "https://example.com/new-image.jpg"
    assert data["data"]["is_primary"] is True


# UPDATE PRODUCT IMAGE - NOT FOUND
@pytest.mark.asyncio
async def test_update_product_image_not_found(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.put(
        "/api/v1/product-images/00000000-0000-0000-0000-000000000000",
        json={
            "product_id": "00000000-0000-0000-0000-000000000000",
            "url": "https://example.com/image.jpg",
            "is_primary": True
        },
        headers=headers
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "product image not found"


# DELETE PRODUCT IMAGE
@pytest.mark.asyncio
async def test_delete_product_image(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    category_response = await client.post(
        "/api/v1/categories/",
        json={"name": "pytest_image_delete_category"},
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["data"]["id"]

    product_response = await client.post(
        "/api/v1/products/",
        json={
            "name": "pytest_image_delete_product",
            "price": 800.00,
            "stock": 10,
            "status": "active",
            "description": "Product for image delete testing",
            "sku": "PYTEST-IMAGE-DELETE-001",
            "category_id": category_id,
            "images": []
        },
        headers=headers
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["data"]["id"]

    create_response = await client.post(
        "/api/v1/product-images/",
        json={
            "product_id": product_id,
            "url": "https://example.com/delete-image.jpg",
            "is_primary": False
        },
        headers=headers
    )

    assert create_response.status_code == 200

    images_response = await client.get(
        "/api/v1/product-images/"
    )

    images = images_response.json()["data"]

    image = next(
        image for image in images
        if image["product_id"] == product_id
    )

    image_id = image["id"]

    response = await client.delete(
        f"/api/v1/product-images/{image_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "product image deleted successfully"

    get_response = await client.get(
        f"/api/v1/product-images/{image_id}"
    )

    assert get_response.status_code == 404


# DELETE PRODUCT IMAGE - NOT FOUND
@pytest.mark.asyncio
async def test_delete_product_image_not_found(admin_client):

    client = admin_client["client"]
    headers = admin_client["headers"]

    response = await client.delete(
        "/api/v1/product-images/00000000-0000-0000-0000-000000000000",
        headers=headers
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "product image not found"