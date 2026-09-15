from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_model import Product


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
    new_product = Product(
        name=name,
        price=price,
        stock=stock,
        status=status,
        description=description,
        sku=sku,
        category_id=category_id
    )

    db.add(new_product)

    await db.commit()
    await db.refresh(new_product)

    return new_product


async def get_products(
    db: AsyncSession
):
    result = await db.execute(
        select(Product)
    )

    return result.scalars().all()


async def get_product_by_id(
    db: AsyncSession,
    product_id: UUID
):
    result = await db.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    return result.scalar_one_or_none()


async def update_product(
    db: AsyncSession,
    product: Product,
    name: str,
    price,
    stock: int,
    status: str,
    description: str,
    sku: str,
    category_id: UUID
):
    product.name = name
    product.price = price
    product.stock = stock
    product.status = status
    product.description = description
    product.sku = sku
    product.category_id = category_id

    await db.commit()
    await db.refresh(product)

    return product


async def delete_product(
    db: AsyncSession,
    product: Product
):
    await db.delete(product)

    await db.commit()