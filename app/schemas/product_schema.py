from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID


class ProductCreate(BaseModel):
    name : str
    price : Decimal
    stock : int
    status : str
    description : str
    sku : str
    category_id: UUID

class ProductUpdate(BaseModel):
    name : str
    price : Decimal
    stock : int
    status : str
    description : str
    sku : str
    category_id: UUID


