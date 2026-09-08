from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)

#post_method

@router.post("/")
async def create_session(session_data: SessionCreate,db: AsyncSession = Depends(get_db)):

    new_session = Session(
        user_id=session_data.user_id,
        token=session_data.token,
        expires_at=session_data.expires_at
    )

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    return {
        "message": "session inserted successfully"
    }

#get_method

@router.get("/")
async def get_sessions(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Session)
    )

    sessions = result.scalars().all()

    return {
        "message": "sessions fetched successfully",
        "data": [
            {
                "id": str(session.id),
                "user_id": str(session.user_id),
                "token": session.token,
                "expires_at": session.expires_at
            }
            for session in sessions
        ]
    }


@router.get("/{session_id}")
async def get_session_using_id( session_id: UUID,db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Session).where(Session.id == session_id))

    session = result.scalar_one_or_none()

    if session is None:
        raise HTTPException( status_code=404,detail="session not found")

    return {
        "message": "session fetched successfully",
        "data": {
            "id": str(session.id),
            "user_id": str(session.user_id),
            "token": session.token,
            "expires_at": session.expires_at
        }
    }

#update_method

@router.put("/{session_id}")
async def update_session(session_id: UUID, session_data: SessionUpdate,db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Session).where(Session.id == session_id)
    )

    session = result.scalar_one_or_none()

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="session not found"
        )

    session.token = session_data.token
    session.expires_at = session_data.expires_at

    await db.commit()
    await db.refresh(session)

    return {
        "message": "session updated successfully"
    }

#delete_method

@router.delete("/{session_id}")
async def delete_session(session_id: UUID,db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Session).where(Session.id == session_id))

    session = result.scalar_one_or_none()

    if session is None:
        raise HTTPException(  status_code=404,detail="session not found" )

    await db.delete(session)
    await db.commit()

    return {
        "message": "session deleted successfully"
    }