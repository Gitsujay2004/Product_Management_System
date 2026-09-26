from uuid import UUID
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Query

from app.database.session import get_db
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services import product_service
from app.api.dependencies import require_admin, get_current_user
from typing import Literal  
from app.schemas.product_response_schema import ProductListResponse,ProductResponse
from app.schemas.common_schema import DataResponse
from app.schemas.common_schema import MessageResponse
from app.exceptions.custom_exceptions import (NotFoundException,   BadRequestException)
import math

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# CREATE PRODUCT
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=DataResponse[ProductResponse])
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(require_admin)
):
    product = await product_service.create_product(
        db=db,
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock,
        status=product_data.status,
        description=product_data.description,
        sku=product_data.sku,
        category_id=product_data.category_id,
        images=product_data.images
    )

    return {
        "message": "Product created successfully",
        "data":product
        # "data": {
        #     "id": str(product.id),
        #     "name": product.name,
        #     "price": product.price,
        #     "stock": product.stock,
        #     "status": product.status,
        #     "description": product.description,
        #     "sku": product.sku,
        #     "category_id": str(product.category_id)
        # }
    }
@router.get(
    "/",
    response_model=ProductListResponse
)
async def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),

    search: str | None = Query(None),

    category_id: UUID | None = Query(None),

    status: str | None = Query(None),

    min_price: Decimal | None = Query(None, ge=0),

    max_price: Decimal | None = Query(None, ge=0),

    sort_by: Literal[
        "name",
        "price",
        "stock",
        "created_at"
    ] = Query("created_at"),

    sort_order: Literal[
        "asc",
        "desc"
    ] = Query("desc"),

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_user)
):

    if min_price is not None and max_price is not None:
        if min_price > max_price:
            raise BadRequestException(
                message="min_price cannot be greater than max_price",
                error_code="INVALID_PRICE_RANGE"
            )

    skip = (page - 1) * limit

    products, total = await product_service.get_products(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        category_id=category_id,
        status=status,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        sort_order=sort_order
    )

    total_pages = math.ceil(total / limit) if total > 0 else 0

    has_next = page < total_pages
    has_previous = page > 1

    return {
        "message": "Products fetched successfully",

        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_previous": has_previous
        },

        "search": search,
        "category_id": category_id,
        "status": status,

        "min_price": min_price,
        "max_price": max_price,

        "sort_by": sort_by,
        "sort_order": sort_order,

        "data": products
    }
#get product by id

@router.get("/{product_id}",response_model=DataResponse[ProductResponse])
async def get_product_by_id(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product = await product_service.get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise NotFoundException(
            message="Product not found",
            error_code="PRODUCT_NOT_FOUND"
        )
    return {
        "message": "Product fetched successfully",
        "data": product
        # "data": {
        #     "id": str(product.id),
        #     "name": product.name,
        #     "price": product.price,
        #     "stock": product.stock,
        #     "status": product.status,
        #     "description": product.description,
        #     "sku": product.sku,
        #     "category_id": str(product.category_id),
        #     "images": [
        #         {
        #             "id": str(image.id),
        #             "url": image.url,
        #             "is_primary": image.is_primary
        #         }
        #         for image in product.images
        #     ]
        # }
    }

# UPDATE PRODUCT
@router.put(
    "/{product_id}",
    response_model=DataResponse[ProductResponse]
)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    product = await product_service.get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
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

    # Fetch again so images are included
    updated_product = await product_service.get_product_by_id(
        db=db,
        product_id=updated_product.id
    )

    return {
        "message": "Product updated successfully",
        "data": updated_product
    }

# DELETE PRODUCT
@router.delete(
    "/{product_id}",
    response_model=MessageResponse
)
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    product = await product_service.get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    await product_service.delete_product(
        db=db,
        product=product
    )

    return {
        "message": "Product deleted successfully"
    }