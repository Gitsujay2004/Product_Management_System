from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import productImage_repo


async def create_product_image(
    db: AsyncSession,
    product_id: UUID,
    url: str,
    is_primary: bool
):
    return await productImage_repo.create_product_image(
        db=db,
        product_id=product_id,
        url=url,
        is_primary=is_primary
    )


async def get_product_images(
    db: AsyncSession
):
    return await productImage_repo.get_product_images(
        db=db
    )


async def get_product_image_by_id(
    db: AsyncSession,
    image_id: UUID
):
    return await productImage_repo.get_product_image_by_id(
        db=db,
        image_id=image_id
    )


async def update_product_image(
    db: AsyncSession,
    product_image,
    product_id: UUID,
    url: str,
    is_primary: bool
):
    return await productImage_repo.update_product_image(
        db=db,
        product_image=product_image,
        product_id=product_id,
        url=url,
        is_primary=is_primary
    )


async def delete_product_image(
    db: AsyncSession,
    product_image
):
    return await productImage_repo.delete_product_image(
        db=db,
        product_image=product_image
    )