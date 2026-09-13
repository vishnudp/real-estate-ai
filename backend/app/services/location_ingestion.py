from typing import Any

from sqlalchemy.orm import Session

from app.models.location import Location


def ingest_location(
    db: Session,
    *,
    name: str,
    location_type: str,
    country: str | None = None,
    city: str | None = None,
    area: str | None = None,
    address: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    source: str = "manual",
    source_url: str | None = None,
    metadata_json: str | None = None,
) -> Location:
    """
    Insert or update a location.

    A location is considered the same when its name,
    location type, city and source match.
    """

    existing = (
        db.query(Location)
        .filter(
            Location.name == name,
            Location.location_type == location_type,
            Location.city == city,
            Location.source == source,
        )
        .first()
    )

    if existing:
        existing.country = country
        existing.area = area
        existing.address = address
        existing.latitude = latitude
        existing.longitude = longitude
        existing.source_url = source_url
        existing.metadata_json = metadata_json

        db.commit()
        db.refresh(existing)

        return existing

    location = Location(
        name=name,
        location_type=location_type,
        country=country,
        city=city,
        area=area,
        address=address,
        latitude=latitude,
        longitude=longitude,
        source=source,
        source_url=source_url,
        metadata_json=metadata_json,
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location


def ingest_locations(
    db: Session,
    locations: list[dict[str, Any]],
) -> list[Location]:
    """
    Bulk-ingest location records.
    """

    results = []

    for item in locations:
        location = ingest_location(
            db,
            name=item["name"],
            location_type=item["location_type"],
            country=item.get("country"),
            city=item.get("city"),
            area=item.get("area"),
            address=item.get("address"),
            latitude=item.get("latitude"),
            longitude=item.get("longitude"),
            source=item.get("source", "manual"),
            source_url=item.get("source_url"),
            metadata_json=item.get("metadata_json"),
        )

        results.append(location)

    return results
