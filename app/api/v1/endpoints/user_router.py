from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.user_schema import UserCreate, UserUpdate,UserStatusUpdate
from app.services import user_service
from app.api.dependencies import require_admin
from app.api.dependencies import get_current_user, require_admin


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
@router.get("/me")
async def get_my_profile(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Profile fetched successfully",
        "user": {
            "id": str(current_user.id),
            "username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at,
            "updated_at": current_user.updated_at
        }
    }


#admin access
@router.get("/{user_id}")
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
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User fetched successfully",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
    }


@router.put("/{user_id}")
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
        raise HTTPException(
            status_code=404,
            detail="User not found"
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
        "user": {
            "id": str(updated_user.id),
            "username": updated_user.username,
            "email": updated_user.email,
            "role": updated_user.role,
            "is_active": updated_user.is_active
        }
    }
@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(require_admin)
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

@router.patch("/{user_id}/status")
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
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    updated_user = await user_service.set_user_active_status(
        db=db,
        user=user,
        is_active=status_data.is_active
    )

    return {
        "message": "User status updated successfully",
        "user": {
            "id": str(updated_user.id),
            "username": updated_user.username,
            "email": updated_user.email,
            "role": updated_user.role,
            "is_active": updated_user.is_active
        }
    }