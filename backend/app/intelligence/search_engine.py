from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.property import Property
from app.knowledge.chroma_store import search as chroma_search


MIN_SEMANTIC_DISTANCE = 0.75


def _normalise_text(value: str | None) -> str:
    return (value or "").strip().lower()


def _contains_value(
    column,
    value: str | None,
):
    """
    SQL LIKE filter helper.
    """

    if not value:
        return None

    return column.ilike(f"%{value}%")


def structured_search(
    db: Session,
    *,
    brand: str | None = None,
    country: str | None = None,
    city: str | None = None,
    property_type: str | None = None,
    limit: int = 5,
) -> list[Property]:
    """
    Search structured property data.

    Brand is stored as JSON in the current schema, so
    SQLite JSON searching is handled through a simple
    text representation for this first implementation.

    Later we can normalize brands into a relational table
    or dedicated indexed column.
    """

    query = db.query(Property)

    filters = []

    if country:
        filters.append(
            Property.country.ilike(
                f"%{country}%"
            )
        )

    if city:
        filters.append(
            Property.city.ilike(
                f"%{city}%"
            )
        )

    if property_type:
        filters.append(
            Property.property_type.ilike(
                f"%{property_type}%"
            )
        )

    if brand:
        # brands is currently JSON.
        #
        # SQLite will represent the JSON array as text,
        # allowing us to perform a case-insensitive match.
        filters.append(
            Property.brands.ilike(
                f"%{brand}%"
            )
        )


    if filters:
        query = query.filter(*filters)

    return (
        query
        .order_by(Property.id.asc())
        .limit(limit)
        .all()
    )


def _property_to_dict(
    property_item: Property,
) -> dict[str, Any]:
    return {
        "id": property_item.id,
        "source": property_item.source,
        "title": property_item.title,
        "project_name": property_item.project_name,
        "developer": property_item.developer,
        "listing_type": property_item.listing_type,
        "property_type": property_item.property_type,
        "country": property_item.country,
        "city": property_item.city,
        "location": property_item.location,
        "price": property_item.price,
        "currency": property_item.currency,
        "bedrooms": property_item.bedrooms,
        "bathrooms": property_item.bathrooms,
        "area": property_item.area,
        "area_unit": property_item.area_unit,
        "status": property_item.status,
        "completion_date": property_item.completion_date,
        "description": property_item.description,
        "amenities": property_item.amenities,
        "brands": property_item.brands,
        "images": property_item.images,
        "source_url": property_item.source_url,
    }


def _chroma_results(
    query: str,
    n_results: int = 5,
) -> list[dict[str, Any]]:
    """
    Semantic retrieval from Chroma.

    We only accept results whose distance is reasonably
    close to the query. This prevents arbitrary queries
    such as "testing" from returning unrelated records.
    """

    if not query.strip():
        return []

    try:
        results = chroma_search(
            query=query,
            n_results=n_results,
        )
    except Exception:
        return []

    documents = (
        results.get("documents") or [[]]
    )[0]

    metadatas = (
        results.get("metadatas") or [[]]
    )[0]

    distances = (
        results.get("distances") or [[]]
    )[0]

    output = []

    for index, document in enumerate(documents):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )

        distance = (
            distances[index]
            if index < len(distances)
            else None
        )

        # If Chroma does not return a distance, keep the
        # result for compatibility.
        if (
            distance is not None
            and distance > MIN_SEMANTIC_DISTANCE
        ):
            continue

        output.append(
            {
                "document": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return output


def hybrid_search(
    db: Session,
    *,
    query: str,
    brand: str | None = None,
    country: str | None = None,
    city: str | None = None,
    property_type: str | None = None,
    limit: int = 5,
) -> dict[str, Any]:
    """
    Hybrid property retrieval.

    Strategy:

    1. Try exact/structured filtering.
    2. If structured results exist, return them.
    3. If no structured results exist, use Chroma semantic
       retrieval.
    4. Never return semantic results for an unknown query.
    """

    structured_results = structured_search(
        db,
        brand=brand,
        country=country,
        city=city,
        property_type=property_type,
        limit=limit,
    )

    if structured_results:
        return {
            "results": [
                _property_to_dict(item)
                for item in structured_results
            ],
            "retrieval_type": "structured",
            "count": len(structured_results),
            "semantic_results": [],
        }

    # Do not perform semantic fallback if the query contains
    # no meaningful property/entity signal.
    has_search_signal = any(
        [
            brand,
            country,
            city,
            property_type,
        ]
    )

    if not has_search_signal:
        return {
            "results": [],
            "retrieval_type": "none",
            "count": 0,
            "semantic_results": [],
        }

    semantic_results = _chroma_results(
        query=query,
        n_results=limit,
    )

    return {
        "results": [],
        "retrieval_type": (
            "semantic"
            if semantic_results
            else "none"
        ),
        "count": len(semantic_results),
        "semantic_results": semantic_results,
    }
