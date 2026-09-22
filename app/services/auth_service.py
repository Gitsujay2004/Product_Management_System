from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime,timedelta,timezone
from app.core.settings import settings  

from app.core.security import create_access_token, hash_password,verify_password,create_refresh_token,verify_access_token,verify_refresh_token
from app.repositories import user_repo,session_repo
from uuid import UUID

async def register_user(
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
            detail="Email already registered"
        )

    hashed_password = hash_password(password)

    return await user_repo.create_user(
        db=db,
        username=username,
        email=email,
        password=hashed_password
    )

async def login_user(db:AsyncSession,email:str,password:str):

    user = await user_repo.get_user_by_email(db=db,email=email)

    if user is None:
        raise HTTPException(status_code=401,detail="Invalid email or password")

    if user is None:
        raise HTTPException(status_code=401,detail="Invalid email or password")

    password_valid = verify_password(password,user.password)

    if not password_valid:
        return None

    token_data = {
        "sub":str(user.id),
        "email":user.email,
        "role":user.role
    }

    access_token = create_access_token( data = token_data)

    refresh_token = create_refresh_token(data=token_data) 

      # Refresh token expiry
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )   

    # Store refresh token in sessions table
    await session_repo.create_session(
        db=db,
        user_id=user.id,
        token=refresh_token,
        expires_at=expires_at
    )
     

    return user,access_token,refresh_token

async def refresh_access_token(
    db: AsyncSession,
    refresh_token: str
):
    # 1. Verify JWT refresh token
    payload = verify_refresh_token(refresh_token)

    if payload is None:
        return None

    # 2. Get user ID from token
    user_id = payload.get("sub")

    if user_id is None:
        return None

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        return None

    # 3. Check refresh token in database
    session = await session_repo.get_session_by_token(
        db=db,
        token=refresh_token
    )

    if session is None:
        return None

    # 4. Check session belongs to same user
    if session.user_id != user_uuid:
        return None

    # 5. Check database session expiry
    if session.expires_at <= datetime.now(timezone.utc):
        await session_repo.delete_session(
            db=db,
            session=session
        )
        return None

    # 6. Check user exists
    user = await user_repo.get_user_by_id(
        db=db,
        user_id=user_uuid
    )

    if user is None:
        return None

    # 7. Create new access token
    token_data = {
        "sub": str(user.id),
        "email": user.email
    }

    new_access_token = create_access_token(
        data=token_data
    )

    return new_access_token

#logout_user

async def logout_user(db:AsyncSession,refresh_token:str):
    session = await session_repo.get_session_by_token(db=db,token=refresh_token)

    if session is None:
        return False
    await session_repo.delete_session(db=db,session=session)
    return True
    