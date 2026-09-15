from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.productImage_schema import ProductImageCreate,ProductImageUpdate
    
    

from app.services import productImage_service


router = APIRouter(
    prefix="/product-images",
    tags=["Product Images"]
)


# CREATE PRODUCT IMAGE

@router.post("/")
async def create_product_image(
    product_image: ProductImageCreate,
    db: AsyncSession = Depends(get_db)
):
    await productImage_service.create_product_image(
        db=db,
        product_id=product_image.product_id,
        url=product_image.url,
        is_primary=product_image.is_primary
    )

    return {
        "message": "product image inserted successfully"
    }


# GET ALL PRODUCT IMAGES

@router.get("/")
async def get_product_images(
    db: AsyncSession = Depends(get_db)
):
    product_images = await productImage_service.get_product_images(
        db=db
    )

    return {
        "message": "product images fetched successfully",
        "data": [
            {
                "id": str(product_image.id),
                "product_id": str(product_image.product_id),
                "url": product_image.url,
                "is_primary": product_image.is_primary
            }
            for product_image in product_images
        ]
    }


# GET PRODUCT IMAGE BY ID

@router.get("/{image_id}")
async def get_product_image_by_id(
    image_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    product_image = await productImage_service.get_product_image_by_id(
        db=db,
        image_id=image_id
    )

    if product_image is None:
        raise HTTPException(
            status_code=404,
            detail="product image not found"
        )

    return {
        "message": "product image fetched successfully",
        "data": {
            "id": str(product_image.id),
            "product_id": str(product_image.product_id),
            "url": product_image.url,
            "is_primary": product_image.is_primary
        }
    }


# UPDATE PRODUCT IMAGE

@router.put("/{image_id}")
async def update_product_image(
    image_id: UUID,
    product_image_data: ProductImageUpdate,
    db: AsyncSession = Depends(get_db)
):
    product_image = await productImage_service.get_product_image_by_id(
        db=db,
        image_id=image_id
    )

    if product_image is None:
        raise HTTPException(
            status_code=404,
            detail="product image not found"
        )

    updated_product_image = await productImage_service.update_product_image(
        db=db,
        product_image=product_image,
        product_id=product_image_data.product_id,
        url=product_image_data.url,
        is_primary=product_image_data.is_primary
    )

    return {
        "message": "product image updated successfully",
        "data": {
            "id": str(updated_product_image.id),
            "product_id": str(updated_product_image.product_id),
            "url": updated_product_image.url,
            "is_primary": updated_product_image.is_primary
        }
    }


# DELETE PRODUCT IMAGE

@router.delete("/{image_id}")
async def delete_product_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    product_image = await productImage_service.get_product_image_by_id(
        db=db,
        image_id=image_id
    )

    if product_image is None:
        raise HTTPException(
            status_code=404,
            detail="product image not found"
        )

    await productImage_service.delete_product_image(
        db=db,
        product_image=product_image
    )

    return {
        "message": "product image deleted successfully"
    }