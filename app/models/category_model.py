import uuid

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.base import Base


class Category(Base):

    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4 
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )