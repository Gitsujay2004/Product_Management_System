from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.services import category_service
from app.api.dependencies import get_current_user,require_admin
from fastapi import status

from app.schemas.category_response_schema import CategoryResponse
from app.schemas.common_schema import DataResponse, MessageResponse
from app.exceptions.custom_exceptions import (NotFoundException,   BadRequestException)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# CREATE CATEGORY
@router.post("/",  status_code=status.HTTP_201_CREATED,response_model=DataResponse[CategoryResponse])
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(require_admin)
):
    await category_service.create_category(
        db=db,
        name=category.name
    )

    return {
        "message": "category inserted successfully",
        "data":category
    }


# GET ALL CATEGORIES
@router.get("/")
async def get_categories(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
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
@router.get(
    "/{category_id}",
    response_model=DataResponse[CategoryResponse]
)
async def get_category_by_id(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    category = await category_service.get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        raise NotFoundException(
            message="Category not found",
            error_code="CATEGORY_NOT_FOUND"
        )
    return {
        "message": "Category fetched successfully",
        "data": category
    }

@router.put(
    "/{category_id}",
    response_model=DataResponse[CategoryResponse]
)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    category = await category_service.get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        raise NotFoundException(
            message="Category not found",
            error_code="CATEGORY_NOT_FOUND"
        )
    
    updated_category = await category_service.update_category(
        db=db,
        category=category,
        name=category_data.name
    )

    return {
        "message": "Category updated successfully",
        "data": updated_category
    }

@router.delete(
    "/{category_id}",
    response_model=MessageResponse
)
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    category = await category_service.get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        raise NotFoundException(
            message="Category not found",
            error_code="CATEGORY_NOT_FOUND"
        )

    await category_service.delete_category(
        db=db,
        category=category
    )

    return {
        "message": "Category deleted successfully"
    }