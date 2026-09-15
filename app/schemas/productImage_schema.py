from uuid import UUID
from pydantic import BaseModel

class ProductImageCreate(BaseModel):
    product_id:UUID
    url:str
    is_primary:bool

class ProductImageUpdate(BaseModel):
    product_id:UUID
    url:str
    is_primary:bool
