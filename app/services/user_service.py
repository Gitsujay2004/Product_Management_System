from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user_repo
from app.core.security import hash_password



from fastapi import HTTPException

from app.core.security import hash_password
from app.repositories import user_repo


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password: str
):
    existing_username = await user_repo.get_user_by_username(
        db=db,
        username=username
    )

    if existing_username is not None:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    existing_email = await user_repo.get_user_by_email(
        db=db,
        email=email
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_password = hash_password(password)

    return await user_repo.create_user(
        db=db,
        username=username,
        email=email,
        password=hashed_password
    )


async def get_users(
    db: AsyncSession
):
    return await user_repo.get_users(
        db=db
    )


async def get_user_by_id(
    db: AsyncSession,
    user_id: UUID
):
    return await user_repo.get_user_by_id(
        db=db,
        user_id=user_id
    )




async def update_user(
    db: AsyncSession,
    user,
    username: str,
    email: str,
    password: str
):
    # Check username
    existing_username = await user_repo.get_user_by_username(
        db=db,
        username=username
    )

    if (
        existing_username is not None
        and existing_username.id != user.id
    ):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check email
    existing_email = await user_repo.get_user_by_email(
        db=db,
        email=email
    )

    if (
        existing_email is not None
        and existing_email.id != user.id
    ):
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Hash new password
    hashed_password = hash_password(password)

    return await user_repo.update_user(
        db=db,
        user=user,
        username=username,
        email=email,
        password=hashed_password
    )


async def delete_user(
    db: AsyncSession,
    user
):
    await user_repo.delete_user(
        db=db,
        user=user
    )

#user deactivate

async def set_user_active_status(
    db: AsyncSession,
    user,
    is_active: bool
):
    return await user_repo.set_user_active_status(
        db=db,
        user=user,
        is_active=is_active
    )
    