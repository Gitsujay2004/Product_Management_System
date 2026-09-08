from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models.product_image import Product_Image
from app.schemas.product_image import ProductImageCreate, ProductImageUpdate


router = APIRouter(
    prefix="/product-images",
    tags=["Product Images"]
)


@router.post("/")
async def create_product_image(
    image_data: ProductImageCreate,
    db: AsyncSession = Depends(get_db)
):
    new_image = Product_Image(
        product_id=image_data.product_id,
        url=image_data.url,
        is_primary=image_data.is_primary
    )

    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)

    return {
        "message": "product image inserted successfully"
    }


@router.get("/")
async def get_product_images(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product_Image)
    )

    images = result.scalars().all()

    return {
        "message": "product images fetched successfully",
        "data": [
            {
                "id": str(image.id),
                "product_id": str(image.product_id),
                "url": image.url,
                "is_primary": image.is_primary
            }
            for image in images
        ]
    }


@router.get("/{image_id}")
async def get_product_image_using_id(
    image_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product_Image).where(Product_Image.id == image_id)
    )

    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="product image not found"
        )

    return {
        "message": "product image fetched successfully",
        "data": {
            "id": str(image.id),
            "product_id": str(image.product_id),
            "url": image.url,
            "is_primary": image.is_primary
        }
    }


@router.put("/{image_id}")
async def update_product_image(
    image_id: UUID,
    image_data: ProductImageUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product_Image).where(Product_Image.id == image_id)
    )

    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="product image not found"
        )

    image.product_id = image_data.product_id
    image.url = image_data.url
    image.is_primary = image_data.is_primary

    await db.commit()
    await db.refresh(image)

    return {
        "message": "product image updated successfully"
    }


@router.delete("/{image_id}")
async def delete_product_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product_Image).where(Product_Image.id == image_id)
    )

    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="product image not found"
        )

    await db.delete(image)
    await db.commit()

    return {
        "message": "product image deleted successfully"
    }