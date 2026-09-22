from pydantic import BaseModel,Field
from decimal import Decimal
from uuid import UUID


class ProductImageRequest(BaseModel):
    url:str
    is_primary : bool = False


class ProductCreate(BaseModel):
    name : str
    price : Decimal
    stock : int
    status : str
    description : str
    sku : str
    category_id: UUID
    images : list[ProductImageRequest] = Field(default_factory=list)

class ProductUpdate(BaseModel):
    name : str
    price : Decimal
    stock : int
    status : str
    description : str
    sku : str
    category_id: UUID


