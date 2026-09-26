from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_access_token
from app.database.session import get_db
from app.repositories import user_repo
from app.exceptions.custom_exceptions import (
    UnauthorizedException,
    ForbiddenException
)



security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
       raise UnauthorizedException(
    message="Invalid or expired token",
    error_code="INVALID_TOKEN"
)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise UnauthorizedException(
    message="Invalid user ID in token",
    error_code="INVALID_TOKEN_USER"
)

    user = await user_repo.get_user_by_id(
    db=db,
    user_id=user_uuid
)

    if user is None:
        raise UnauthorizedException(
    message="User not found",
    error_code="TOKEN_USER_NOT_FOUND"
)

    if not user.is_active:
       raise ForbiddenException(
    message="User account is inactive",
    error_code="ACCOUNT_INACTIVE"
)
    return user

async def require_admin(
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise ForbiddenException(
    message="Admin access required",
    error_code="ADMIN_ACCESS_REQUIRED"
)

    return current_user