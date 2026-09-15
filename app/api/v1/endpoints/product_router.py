from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# CREATE PRODUCT
@router.post("/")
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    await product_service.create_product(
        db=db,
        name=product.name,
        price=product.price,
        stock=product.stock,
        status=product.status,
        description=product.description,
        sku=product.sku,
        category_id=product.category_id
    )

    return {
        "message": "product inserted successfully"
    }


# GET ALL PRODUCTS
@router.get("/")
async def get_products(
    db: AsyncSession = Depends(get_db)
):
    products = await product_service.get_products(
        db=db
    )

    return {
        "message": "fetched successfully",
        "data": [
            {
                "id": str(product.id),
                "product_name": product.name
            }
            for product in products
        ]
    }


# GET PRODUCT BY ID
@router.get("/{product_id}")
async def get_product_by_id(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    product = await product_service.get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )

    return {
        "message": "product fetched successfully",
        "data": {
            "id": str(product.id),
            "name": product.name
        }
    }


# UPDATE PRODUCT
@router.put("/{product_id}")
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    product = await product_service.get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )

    updated_product = await product_service.update_product(
        db=db,
        product=product,
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock,
        status=product_data.status,
        description=product_data.description,
        sku=product_data.sku,
        category_id=product_data.category_id
    )

    return {
        "message": "product updated successfully",
        "data": {
            "id": str(updated_product.id),
            "name": updated_product.name,
            "price": updated_product.price
        }
    }


# DELETE PRODUCT
@router.delete("/{product_id}")
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    product = await product_service.get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )

    await product_service.delete_product(
        db=db,
        product=product
    )

    return {
        "message": "successfully deleted"
    }