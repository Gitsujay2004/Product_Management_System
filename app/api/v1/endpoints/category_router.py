from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.services import category_service


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# CREATE CATEGORY
@router.post("/")
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    await category_service.create_category(
        db=db,
        name=category.name
    )

    return {
        "message": "category inserted successfully"
    }


# GET ALL CATEGORIES
@router.get("/")
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    categories = await category_service.get_categories(
        db=db
    )

    return {
        "message": "categories fetched successfully",
        "data": [
            {
                "id": str(category.id),
                "name": category.name
            }
            for category in categories
        ]
    }


# GET CATEGORY BY ID
@router.get("/{category_id}")
async def get_category_by_id(
    category_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    category = await category_service.get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="category not found"
        )

    return {
        "message": "category fetched successfully",
        "data": {
            "id": str(category.id),
            "name": category.name
        }
    }


# UPDATE CATEGORY
@router.put("/{category_id}")
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    category = await category_service.get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="category not found"
        )

    updated_category = await category_service.update_category(
        db=db,
        name=category_data.name,
        category=category
    )

    return {
        "message": "category updated successfully",
        "data": {
            "id": str(updated_category.id),
            "name": updated_category.name
        }
    }


# DELETE CATEGORY
@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    category = await category_service.get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="category not found"
        )

    await category_service.delete_category(
        db=db,
        category=category
    )

    return {
        "message": "category deleted successfully"
    }