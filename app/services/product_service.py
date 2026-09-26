from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import product_repo

from decimal import Decimal


async def create_product(
    db: AsyncSession,
    name: str,
    price,
    stock: int,
    status: str,
    description: str,
    sku: str,
    category_id: UUID,
    images
):
    return await product_repo.create_product(
        db=db,
        name=name,
        price=price,
        stock=stock,
        status=status,
        description=description,
        sku=sku,
        category_id=category_id,
        images=images
    )
    return await product_repo.get_product_by_id(
        db=db,
        product_id=product.id
    )

async def get_products(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    category_id: UUID | None = None,
    status: str | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    return await product_repo.get_products(
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