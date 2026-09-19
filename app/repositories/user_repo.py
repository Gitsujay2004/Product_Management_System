from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User


async def create_user(db: AsyncSession,username: str,email: str,password: str):
    new_user = User(
        username=username,
        email=email,
        password=password
    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_users( db: AsyncSession):

    result = await db.execute(
        select(User)
    )

    return result.scalars().all()


async def get_user_by_id(db: AsyncSession,user_id: UUID):

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    return result.scalar_one_or_none()

async def get_user_by_email(db:AsyncSession,email:str):
    result =  await db.execute(select(User).where(User.email==email))
    return result.scalar_one_or_none()



async def update_user(
    db: AsyncSession,
    user: User,
    username: str,
    email: str,
    password: str
):
    user.username = username
    user.email = email
    user.password = password

    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(
    db: AsyncSession,
    user: User
):
    await db.delete(user)
    await db.commit()