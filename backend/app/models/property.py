from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base


if TYPE_CHECKING:
    from app.models.location import Location


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        index=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String(255),
        index=True,
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(500),
    )

    project_name: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    developer: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    listing_type: Mapped[str | None] = mapped_column(
        String(50),
        index=True,
        nullable=True,
    )

    property_type: Mapped[str | None] = mapped_column(
        String(100),
        index=True,
        nullable=True,
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

    location: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )


    price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    currency: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    bedrooms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    bathrooms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    area: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    area_unit: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    status: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    completion_date: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    amenities: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    brands: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    images: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    source_url: Mapped[str] = mapped_column(
        String(1000),
    )

    raw_content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    scraped_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    location_id: Mapped[int | None] = mapped_column(
        ForeignKey("locations.id"),
        nullable=True,
        index=True,
    )

    location_record: Mapped["Location | None"] = relationship(
        "Location",
        foreign_keys=[location_id],
    )

