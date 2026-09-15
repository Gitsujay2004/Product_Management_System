from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import product_repo


async def create_product(
    db: AsyncSession,
    name: str,
    price,
    stock: int,
    status: str,
    description: str,
    sku: str,
    category_id: UUID
):
    return await product_repo.create_product(
        db=db,
        name=name,
        price=price,
        stock=stock,
        status=status,
        description=description,
        sku=sku,
        category_id=category_id
    )


async def get_products(
    db: AsyncSession
):
    return await product_repo.get_products(
        db=db
    )


async def get_product_by_id(
    db: AsyncSession,
    product_id: UUID
):
    return await product_repo.get_product_by_id(
        db=db,
        product_id=product_id
    )


async def update_product(
    db: AsyncSession,
    product,
    name: str,
    price,
    stock: int,
    status: str,
    description: str,
    sku: str,
    category_id: UUID
):
    return await product_repo.update_product(
        db=db,
        product=product,
        name=name,
        price=price,
        stock=stock,
        status=status,
        description=description,
        sku=sku,
        category_id=category_id
    )


async def delete_product(
    db: AsyncSession,
    product
):
    await product_repo.delete_product(
        db=db,
        product=product
    )