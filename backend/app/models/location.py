from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.property import Property


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        index=True,
    )

    location_type: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        index=True,
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(150),
        index=True,
        nullable=True,
    )

    area: Mapped[str | None] = mapped_column(
        String(255),
        index=True,
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    source: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    metadata_json: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    properties: Mapped[list["Property"]] = relationship(
        "Property",
        foreign_keys="Property.location_id",
        back_populates="location_record",
    )
