import uuid
from sqlalchemy import String,DateTime,ForeignKey,Integer,Numeric,Text
from decimal import Decimal
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.sql import func

from app.database.database import Base

class Product(Base):

    __tablename__ = "products"

    id : Mapped[uuid.UUID] = mapped_column(primary_key = True,default=uuid.uuid4)

    name : Mapped[str] = mapped_column(String(100),unique=True,nullable=False)

    category_id : Mapped[uuid.UUID ] = mapped_column(ForeignKey("categories.id"),nullable=False)

    price : Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)

    stock : Mapped[int] = mapped_column(Integer,nullable=False)

    status : Mapped[str ]= mapped_column(String(20),nullable=False)

    description : Mapped[str] = mapped_column(Text)

    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())

    updated_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

    sku : Mapped[str] = mapped_column(String(100),nullable=False)

