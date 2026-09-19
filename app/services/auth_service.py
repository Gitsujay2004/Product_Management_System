from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password,verify_password
from app.repositories import user_repo

async def register_user(db:AsyncSession,username:str,email:str,password:str):
    existing_user  = await user_repo.get_user_by_email(db=db,email=email)

    if existing_user is not None:
        raise HTTPException(status_code=400,detail="Email already registered")

    hashed_password = hash_password(password)

    return await user_repo.create_user(db=db,username=username,email=email,password=hashed_password)

async def login_user(db:AsyncSession,email:str,password:str):

    user = await user_repo.get_user_by_email(db=db,email=email)

    if user is None:
        raise HTTPException(status_code=401,detail="Invalid email or password")

    password_valid = verify_password(password,user.password)

    if not password_valid:
        raise HTTPException(status_code=401,detail="Invalid email or password")

    return user




