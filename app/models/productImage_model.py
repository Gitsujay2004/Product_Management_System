import uuid
from sqlalchemy import String,DateTime,Boolean,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.sql import func

from app.database.base import Base

class ProductImage(Base):
    
    __tablename__ = "product_image"

    id:Mapped[uuid.UUID] = mapped_column(primary_key = True,default = uuid.uuid4)

    product_id:Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"),nullable=False)

    url:Mapped[str] = mapped_column(String(100),nullable = False)

    is_primary:Mapped[bool]  = mapped_column(Boolean)

    created_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())

    updated_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())