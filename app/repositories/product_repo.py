from uuid import UUID
from decimal import Decimal

from sqlalchemy import select,func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_model import Product
from app.models.productImage_model import ProductImage

from sqlalchemy import select, func,asc,desc





# CREATE PRODUCT + IMAGES
async def create_product(
    db: AsyncSession,
    name: str,
    price: Decimal,
    stock: int,
    status: str,
    description: str,
    sku: str,
    category_id: UUID,
    images
):
    # 1. Create product
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

    # Generate product ID before creating images
    await db.flush()

    # 2. Create product images
    for image in images:
        new_image = ProductImage(
            product_id=new_product.id,
            url=image.url,
            is_primary=image.is_primary
        )

        db.add(new_image)

    # 3. Save product + images
    await db.commit()

    # Refresh product
    await db.refresh(new_product)

    return new_product



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
    query = select(Product)
    count_query = select(func.count(Product.id))

    # Search
    if search:
        condition = Product.name.ilike(f"%{search}%")
        query = query.where(condition)
        count_query = count_query.where(condition)

    # Category filter
    if category_id:
        condition = Product.category_id == category_id
        query = query.where(condition)
        count_query = count_query.where(condition)

    # Status filter
    if status:
        condition = Product.status == status
        query = query.where(condition)
        count_query = count_query.where(condition)

    # Minimum price
    if min_price is not None:
        condition = Product.price >= min_price
        query = query.where(condition)
        count_query = count_query.where(condition)

    # Maximum price
    if max_price is not None:
        condition = Product.price <= max_price
        query = query.where(condition)
        count_query = count_query.where(condition)

    # Count
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # Sorting
    sort_columns = {
        "name": Product.name,
        "price": Product.price,
        "stock": Product.stock,
        "created_at": Product.created_at
    }

    sort_column = sort_columns.get(sort_by, Product.created_at) #sort_by get from user it is worng - default => Product.created_at

    if sort_order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # Pagination
    result = await db.execute(
        query
        .options(selectinload(Product.images))
        .offset(skip)
        .limit(limit)
    )

    products = result.scalars().all()

    return products, total

# GET PRODUCT BY ID
async def get_product_by_id(
    db: AsyncSession,
    product_id: UUID
):
    result = await db.execute(
        select(Product)
        .options(
            selectinload(Product.images)
        )
        .where(
            Product.id == product_id
        )
    )

    return result.scalar_one_or_none()


# UPDATE PRODUCT
async def update_product(
    db: AsyncSession,
    product: Product,
    name: str,
    price: Decimal,
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


# DELETE PRODUCT
async def delete_product(
    db: AsyncSession,
    product: Product
):
    await db.delete(product)

    await db.commit()