from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
async def create_user(user: UserCreate,db: AsyncSession = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {
        "message": "user inserted successfully"
    }

#get method

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User))

    users = result.scalars().all()

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

#get_method_using_spcific_id

@router.get("/{user_id}")
async def get_user_using_id(  user_id: UUID,db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).where(User.id == user_id) )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404,detail="user not found")

    return {
        "message": "user fetched successfully",
        "data": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active
        }
    }


#update method

@router.put("/{user_id}")
async def update_user(user_id: UUID,user_data: UserUpdate,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    user.username = user_data.username
    user.email = user_data.email
    user.password = user_data.password

    await db.commit()
    await db.refresh(user)

    return {
        "message": "user updated successfully"
    }


@router.delete("/{user_id}")
async def delete_user( user_id: UUID,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    await db.delete(user)
    await db.commit()

    return {
        "message": "user deleted successfully"
    }