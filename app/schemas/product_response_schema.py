from decimal import Decimal
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductImageResponse(BaseModel):
    id: UUID
    url: str
    is_primary: bool

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    id: UUID
    name: str
    price: Decimal
    stock: int
    status: str
    description: str | None
    sku: str
    category_id: UUID
    created_at: datetime
    updated_at: datetime
    images: list[ProductImageResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ProductListResponse(BaseModel):
    message: str
    page: int
    limit: int
    total: int
    search: str | None
    category_id: UUID | None
    status: str | None
    min_price: Decimal | None
    max_price: Decimal | None
    sort_by: str
    sort_order: str
    data: list[ProductResponse]