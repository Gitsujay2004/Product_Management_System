import uuid

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.base import Base


class Session(Base):

    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    token: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    expires_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
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