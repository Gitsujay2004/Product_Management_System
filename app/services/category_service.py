from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession 

from app.repositories import category_repo

async def create_category(db: AsyncSession,name:str):
    return await category_repo.create_category(
        db=db,
        name=name

    )

async def get_categories(db:AsyncSession):

    return await category_repo.get_categories(db=db)

async def get_category_by_id(db:AsyncSession,category_id:UUID):
    return await category_repo.get_category_by_id(db=db,category_id=category_id)

async def update_category(db:AsyncSession,name:str,category):
    return await category_repo.update_category(
        db=db,
        name=name,
        category=category
    )

async def delete_category(db:AsyncSession,category):
    return await category_repo.delete_category(
        db=db,
        category=category
                                        
    )

