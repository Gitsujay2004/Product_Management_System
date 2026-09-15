from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.session_schema import (
    SessionCreate,
    SessionUpdate
)
from app.services import session_service


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


# CREATE SESSION

@router.post("/")
async def create_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db)
):
    await session_service.create_session(
        db=db,
        user_id=session_data.user_id,
        token=session_data.token,
        expires_at=session_data.expires_at
    )

    return {
        "message": "session inserted successfully"
    }


# GET ALL SESSIONS

@router.get("/")
async def get_sessions(
    db: AsyncSession = Depends(get_db)
):
    sessions = await session_service.get_sessions(
        db=db
    )

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


# GET SESSION BY ID

@router.get("/{session_id}")
async def get_session_by_id(
    session_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    session = await session_service.get_session_by_id(
        db=db,
        session_id=session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="session not found"
        )

    return {
        "message": "session fetched successfully",
        "data": {
            "id": str(session.id),
            "user_id": str(session.user_id),
            "token": session.token,
            "expires_at": session.expires_at
        }
    }


# UPDATE SESSION

@router.put("/{session_id}")
async def update_session(
    session_id: UUID,
    session_data: SessionUpdate,
    db: AsyncSession = Depends(get_db)
):
    session = await session_service.get_session_by_id(
        db=db,
        session_id=session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="session not found"
        )

    updated_session = await session_service.update_session(
        db=db,
        session=session,
        token=session_data.token,
        expires_at=session_data.expires_at
    )

    return {
        "message": "session updated successfully",
        "data": {
            "id": str(updated_session.id),
            "token": updated_session.token,
            "expires_at": updated_session.expires_at
        }
    }


# DELETE SESSION

@router.delete("/{session_id}")
async def delete_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    session = await session_service.get_session_by_id(
        db=db,
        session_id=session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="session not found"
        )

    await session_service.delete_session(
        db=db,
        session=session
    )

    return {
        "message": "session deleted successfully"
    }