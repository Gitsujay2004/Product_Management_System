from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category_model import Category

async def create_category(db:AsyncSession,categoryname:str):
    new_category = Category(
        name=categoryname
    )

    db.add(new_category)

    await db.commit()
    await db.refresh(new_category)
    return new_category

async def get_categories(db:AsyncSession):

    result = await db.execute(select(Category))

    return result.scalars().all()

async def get_category_by_id(db:AsyncSession,category_id:UUID):

    result = await db.execute(select(Category).where(Category.id == category_id ))

    return result.scalar_one_or_none()

async def update_category(db:AsyncSession,category : Category,name:str):
    category.name = name

    await db.commit()
    await db.refresh(category)

    return category

async def delete_category(db:AsyncSession,category : Category):

    await db.delete(category)
    await db.commit()

