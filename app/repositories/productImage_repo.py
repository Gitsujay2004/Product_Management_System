from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.productImage_model import ProductImage


async def productImage_repo(
    db: AsyncSession,
    product_id: UUID,
    url: str,
    is_primary: bool
):
    new_product_image = ProductImage(
        product_id=product_id,
        url=url,
        is_primary=is_primary
    )

    db.add(new_product_image)

    await db.commit()
    await db.refresh(new_product_image)

    return new_product_image


async def get_product_images(
    db: AsyncSession
):
    result = await db.execute(
        select(ProductImage)
    )

    return result.scalars().all()


async def get_product_image_by_id(
    db: AsyncSession,
    image_id: UUID
):
    result = await db.execute(
        select(ProductImage).where(
            ProductImage.id == image_id
        )
    )

    return result.scalar_one_or_none()


async def update_product_image(
    db: AsyncSession,
    product_image: ProductImage,
    product_id: UUID,
    url: str,
    is_primary: bool
):
    product_image.product_id = product_id
    product_image.url = url
    product_image.is_primary = is_primary

    await db.commit()
    await db.refresh(product_image)

    return product_image


async def delete_product_image(
    db: AsyncSession,
    product_image: ProductImage
):
    await db.delete(product_image)

    await db.commit()