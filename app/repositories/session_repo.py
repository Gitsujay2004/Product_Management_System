from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session_model import Session


async def create_session(
    db: AsyncSession,
    user_id: UUID,
    token: str,
    expires_at
):
    new_session = Session(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )

    db.add(new_session)

    await db.commit()
    await db.refresh(new_session)

    return new_session


async def get_sessions(
    db: AsyncSession
):
    result = await db.execute(
        select(Session)
    )

    return result.scalars().all()


async def get_session_by_id(
    db: AsyncSession,
    session_id: UUID
):
    result = await db.execute(
        select(Session).where(
            Session.id == session_id
        )
    )

    return result.scalar_one_or_none()


async def update_session(
    db: AsyncSession,
    session: Session,
    token: str,
    expires_at
):
    session.token = token
    session.expires_at = expires_at

    await db.commit()
    await db.refresh(session)

    return session


async def delete_session(
    db: AsyncSession,
    session: Session
):
    await db.delete(session)

    await db.commit()