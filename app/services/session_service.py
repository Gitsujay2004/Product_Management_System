from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import session_repo


async def create_session(
    db: AsyncSession,
    user_id: UUID,
    token: str,
    expires_at: datetime
):
    return await session_repo.create_session(
        db=db,
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )


async def get_sessions(
    db: AsyncSession
):
    return await session_repo.get_sessions(
        db=db
    )


async def get_session_by_id(
    db: AsyncSession,
    session_id: UUID
):
    return await session_repo.get_session_by_id(
        db=db,
        session_id=session_id
    )


async def update_session(
    db: AsyncSession,
    session,
    token: str,
    expires_at: datetime
):
    return await session_repo.update_session(
        db=db,
        session=session,
        token=token,
        expires_at=expires_at
    )


async def delete_session(
    db: AsyncSession,
    session
):
    return await session_repo.delete_session(
        db=db,
        session=session
    )