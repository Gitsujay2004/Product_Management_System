from decimal import Decimal
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict,Field

from math import ceil



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


class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool

class ProductListResponse(BaseModel):
    message: str

    pagination: PaginationResponse

    search: str | None
    category_id: UUID | None
    status: str | None
    min_price: Decimal | None
    max_price: Decimal | None
    sort_by: str
    sort_order: str

    data: list[ProductResponse]