from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.user_schema import UserCreate, UserUpdate
from app.services import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    await user_service.create_user(
        db=db,
        username=user.username,
        email=user.email,
        password=user.password
    )

    return {
        "message": "user inserted successfully"
    }


@router.get("/")
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    users = await user_service.get_users(
        db=db
    )

    return {
        "message": "users fetched successfully",
        "data": [
            {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active
            }
            for user in users
        ]
    }


@router.get("/{user_id}")
async def get_user_using_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    user = await user_service.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    return {
        "message": "user fetched successfully",
        "data": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active
        }
    }


@router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user = await user_service.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    await user_service.update_user(
        db=db,
        user=user,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )

    return {
        "message": "user updated successfully"
    }


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    user = await user_service.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    await user_service.delete_user(
        db=db,
        user=user
    )

    return {
        "message": "user deleted successfully"
    }