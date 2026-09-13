from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.property import Property


def parse_float(value: Any) -> float | None:
    if value is None or value == "":
        return None

    if isinstance(value, (int, float)):
        return float(value)

    try:
        text = str(value).replace(",", "").strip()

        # Extract the first numeric value.
        import re

        match = re.search(
            r"\d+(?:\.\d+)?",
            text,
        )

        if not match:
            return None

        return float(match.group())

    except (TypeError, ValueError):
        return None


def parse_int(value: Any) -> int | None:
    if value is None or value == "":
        return None

    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None

    if isinstance(value, datetime):
        return value

    try:
        return datetime.fromisoformat(
            str(value).replace("Z", "+00:00")
        ).replace(tzinfo=None)

    except (TypeError, ValueError):
        return None


def normalize_list(value: Any) -> list[str] | None:
    if value is None:
        return None

    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return None

        return [value]

    return [str(value)]


def upsert_property(
    db: Session,
    record: dict,
) -> Property | None:

    source_url = record.get("source_url")

    if not source_url:
        return None

    # --------------------------------------------------------
    # Only actual property/project records belong in the
    # structured Property table.
    #
    # Category pages, home pages, press releases, etc. can
    # still be stored in Chroma for semantic search, but
    # must not become Property rows.
    # --------------------------------------------------------

    property_name = (
        record.get("property_name")
        or record.get("project_name")
    )

    if not property_name:
        return None

    if not record.get("property_type"):
        return None

    if not record.get("country"):
        return None

    existing = (
        db.query(Property)
        .filter(
            Property.source_url == source_url
        )
        .first()
    )

    if existing:
        property_item = existing
    else:
        property_item = Property(
            source_url=source_url
        )

        db.add(property_item)

    property_item.source = str(
        record.get("source") or ""
    )

    property_item.external_id = (
        record.get("external_id")
    )

    property_item.title = str(
        record.get("title") or ""
    )

    property_item.project_name = property_name

    property_item.developer = (
        record.get("developer")
    )

    property_item.listing_type = (
        record.get("listing_type")
    )

    property_item.property_type = (
        record.get("property_type")
    )

    property_item.country = (
        record.get("country")
    )

    property_item.city = (
        record.get("city")
    )

    property_item.location = (
        record.get("location")
    )



def upsert_properties(
    db: Session,
    records: list[dict],
) -> int:

    count = 0

    for record in records:

        property_item = upsert_property(
            db=db,
            record=record,
        )

        if property_item:
            count += 1

    db.commit()

    return count
