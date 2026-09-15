from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user_repo


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password: str
):
    return await user_repo.create_user(
        db=db,
        username=username,
        email=email,
        password=password
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
    return await user_repo.update_user(
        db=db,
        user=user,
        username=username,
        email=email,
        password=password
    )


async def delete_user(
    db: AsyncSession,
    user
):
     return await user_repo.delete_user(
        db=db,
        user=user
    )