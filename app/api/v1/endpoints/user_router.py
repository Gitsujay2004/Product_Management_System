from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.user_schema import UserCreate, UserUpdate,UserStatusUpdate
from app.services import user_service
from app.api.dependencies import require_admin
from app.api.dependencies import get_current_user, require_admin
from app.schemas.user_response_schema import UserResponse
from app.schemas.common_schema import DataResponse, MessageResponse
from app.exceptions.custom_exceptions import (NotFoundException,   BadRequestException)



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/",  status_code=status.HTTP_201_CREATED)
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

# own user access
@router.get(
    "/me",
    response_model=DataResponse[UserResponse]
)
async def get_my_profile(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Profile fetched successfully",
        "data": current_user
    }


#admin access
@router.get(
    "/{user_id}",
    response_model=DataResponse[UserResponse]
)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    user = await user_service.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise NotFoundException(
    message="User not found",
    error_code="USER_NOT_FOUND"
        )

    return {
        "message": "User fetched successfully",
        "data": user
    }

@router.put(
    "/{user_id}",
    response_model=DataResponse[UserResponse]
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    user = await user_service.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise NotFoundException(
    message="User not found",
    error_code="USER_NOT_FOUND"
      )

    updated_user = await user_service.update_user(
        db=db,
        user=user,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )

    return {
        "message": "User updated successfully",
        "data": updated_user
    }

@router.delete(
    "/{user_id}",
    response_model=MessageResponse
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    user = await user_service.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise NotFoundException(
    message="User not found",
    error_code="USER_NOT_FOUND"
       )

    await user_service.delete_user(
        db=db,
        user=user
    )

    return {
        "message": "User deleted successfully"
    }

@router.patch("/{user_id}/status",response_model=DataResponse[UserResponse])
async def update_user_status(
    user_id: UUID,
    status_data: UserStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    user = await user_service.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise NotFoundException(
    message="User not found",
    error_code="USER_NOT_FOUND"
      )

    updated_user = await user_service.set_user_active_status(
        db=db,
        user=user,
        is_active=status_data.is_active
    )

    return {
        "message": "User status updated successfully",
        "data":updated_user
    }