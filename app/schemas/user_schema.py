from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=100
    )


class UserUpdate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=100
    )


class UserStatusUpdate(BaseModel):
    is_active: bool