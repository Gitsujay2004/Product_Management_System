from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession 

from app.repositories import category_repo

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import category_repo


async def create_category(
    db: AsyncSession,
    name: str
):
    existing_category = await category_repo.get_category_by_name(
        db=db,
        name=name
    )

    if existing_category is not None:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    return await category_repo.create_category(
        db=db,
        categoryname=name
    )

async def get_categories(db:AsyncSession):

    return await category_repo.get_categories(db=db)

async def get_category_by_id(db:AsyncSession,category_id:UUID):
    return await category_repo.get_category_by_id(db=db,category_id=category_id)

async def update_category(
    db: AsyncSession,
    category,
    name: str
):
    existing_category = await category_repo.get_category_by_name(
        db=db,
        name=name
    )

    if (
        existing_category is not None
        and existing_category.id != category.id
    ):
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    return await category_repo.update_category(
        db=db,
        category=category,
        name=name
    )

from fastapi import HTTPException


async def delete_category(
    db: AsyncSession,
    category
):
    has_products = await category_repo.category_has_products(
        db=db,
        category_id=category.id
    )

    if has_products:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category because products are assigned to it"
        )

    await category_repo.delete_category(
        db=db,
        category=category
    )

    return True
