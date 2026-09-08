 

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# ===================================
# CREATE CATEGORY
# POST /categories/
# ===================================

@router.post("/")
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):

    new_category = Category(
        name=category.name
    )

    db.add(new_category)

    await db.commit()

    await db.refresh(new_category)

    return {
        "message": "Category created successfully",
        "data": {
            "id": str(new_category.id),
            "name": new_category.name
        }
    }


# ===================================
# GET ALL CATEGORIES
# GET /categories/
# ===================================

@router.get("/")
async def get_categories(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Category)
    )

    categories = result.scalars().all()

    return {
        "message": "Categories fetched successfully",
        "data": [
            {
                "id": str(category.id),
                "name": category.name
            }
            for category in categories
        ]
    }


# ===================================
# GET CATEGORY BY ID
# GET /categories/{category_id}
# ===================================

@router.get("/{category_id}")
async def get_category_by_id(
    category_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Category).where(
            Category.id == category_id
        )
    )

    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return {
        "message": "Category fetched successfully",
        "data": {
            "id": str(category.id),
            "name": category.name
        }
    }


# ===================================
# UPDATE CATEGORY
# PUT /categories/{category_id}
# ===================================

@router.put("/{category_id}")
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Category).where(
            Category.id == category_id
        )
    )

    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category.name = category_data.name

    await db.commit()

    await db.refresh(category)

    return {
        "message": "Category updated successfully",
        "data": {
            "id": str(category.id),
            "name": category.name
        }
    }


# ===================================
# DELETE CATEGORY
# DELETE /categories/{category_id}
# ===================================

@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Category).where(
            Category.id == category_id
        )
    )

    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    await db.delete(category)

    await db.commit()

    return {
        "message": "Category deleted successfully"
    }