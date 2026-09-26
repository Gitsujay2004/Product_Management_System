from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, field_validator


class ProductImageRequest(BaseModel):
    url: HttpUrl
    is_primary: bool = False


class ProductCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    price: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2
    )

    stock: int = Field(
        ...,
        ge=0
    )

    status: str = Field(
        ...,
        min_length=2,
        max_length=20
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=2000
    )

    sku: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    category_id: UUID

    images: list[ProductImageRequest] = Field(
        default_factory=list
    )

    @field_validator("name", "sku", "status", "description")
    @classmethod
    def remove_extra_spaces(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value


class ProductUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    price: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2
    )

    stock: int = Field(
        ...,
        ge=0
    )

    status: str = Field(
        ...,
        min_length=2,
        max_length=20
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=2000
    )

    sku: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    category_id: UUID

    @field_validator("name", "sku", "status", "description")
    @classmethod
    def remove_extra_spaces(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value