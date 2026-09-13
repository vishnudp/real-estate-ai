from typing import Any

from sqlalchemy.orm import Session

from app.models.property import Property
from app.knowledge.chroma_store import search as chroma_search
from app.services.query_understanding import understand_query


MIN_SEMANTIC_DISTANCE = 1.2


PROPERTY_TYPE_ALIASES = {
    "residence": "hotel_residences",
    "residences": "hotel_residences",
    "hotel residence": "hotel_residences",
    "hotel residences": "hotel_residences",
    "branded residence": "hotel_residences",
    "branded residences": "hotel_residences",

    "apartment": "apartments",
    "apartments": "apartments",

    "villa": "villas",
    "villas": "villas",

    "hotel resort": "hotel_resort",
    "hotel & resort": "hotel_resort",
    "hotel and resort": "hotel_resort",
    "resort": "hotel_resort",
}


def normalize_property_type(
    value: str | None,
) -> str | None:
    """
    Convert user-facing property type aliases into the
    canonical values used by the database.
    """

    if not value:
        return None

    normalized = value.strip().lower()

    return PROPERTY_TYPE_ALIASES.get(
        normalized,
        value,
    )


def structured_search(
    db: Session,
    *,
    brand: str | None = None,
    country: str | None = None,
    city: str | None = None,
    property_type: str | None = None,
    bedrooms: int | None = None,
    bathrooms: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_area: float | None = None,
    max_area: float | None = None,
    listing_type: str | None = None,
    status: str | None = None,
    limit: int = 5,
) -> list[Property]:
    """
    Search actual Property records using structured filters.
    """

    query = db.query(Property)

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    if country:
        query = query.filter(
            Property.country.ilike(
                f"%{country}%"
            )
        )

    if city:
        query = query.filter(
            Property.city.ilike(
                f"%{city}%"
            )
        )

    # --------------------------------------------------------
    # Property
    # --------------------------------------------------------

    if property_type:
        canonical_type = normalize_property_type(
            property_type
        )

        query = query.filter(
            Property.property_type.ilike(
                f"%{canonical_type}%"
            )
        )

    if brand:
        query = query.filter(
            Property.brands.ilike(
                f"%{brand}%"
            )
        )

    # --------------------------------------------------------
    # Bedrooms / bathrooms
    # --------------------------------------------------------

    if bedrooms is not None:
        query = query.filter(
            Property.bedrooms == bedrooms
        )

    if bathrooms is not None:
        query = query.filter(
            Property.bathrooms >= bathrooms
        )

    # --------------------------------------------------------
    # Price
    # --------------------------------------------------------

    if min_price is not None:
        query = query.filter(
            Property.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            Property.price <= max_price
        )

    # --------------------------------------------------------
    # Area
    # --------------------------------------------------------

    if min_area is not None:
        query = query.filter(
            Property.area >= min_area
        )

    if max_area is not None:
        query = query.filter(
            Property.area <= max_area
        )

    # --------------------------------------------------------
    # Listing / status
    # --------------------------------------------------------

    if listing_type:
        query = query.filter(
            Property.listing_type.ilike(
                f"%{listing_type}%"
            )
        )

    if status:
        query = query.filter(
            Property.status.ilike(
                f"%{status}%"
            )
        )

    return (
        query
        .order_by(Property.id.asc())
        .limit(limit)
        .all()
    )



def _property_to_dict(
    property_item: Property,
) -> dict[str, Any]:
    """
    Convert SQLAlchemy Property into API-safe dictionary.
    """

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
    filters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """
    Retrieve semantically similar documents from Chroma.
    """

    if not query.strip():
        return []

    try:
        results = chroma_search(
            query=query,
            n_results=n_results,
            filters=filters,
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

        if (
            distance is not None
            and distance > MIN_SEMANTIC_DISTANCE
        ):
            continue

        document_type = (
            metadata.get("document_type")
            or "general"
        )

        output.append(
            {
                "document": document,
                "metadata": metadata,
                "distance": distance,
                "document_type": document_type,
            }
        )

    return output


def _is_same_property(
    semantic_item: dict[str, Any],
    structured_item: dict[str, Any],
) -> bool:
    """
    Determine whether a semantic document represents the
    same property already returned by SQL.
    """

    metadata = semantic_item.get(
        "metadata",
        {},
    )

    semantic_url = (
        metadata.get("source_url")
        or ""
    ).strip().lower()

    structured_url = (
        structured_item.get("source_url")
        or ""
    ).strip().lower()

    if (
        semantic_url
        and structured_url
        and semantic_url == structured_url
    ):
        return True

    semantic_property = (
        metadata.get("property_name")
        or ""
    ).strip().lower()

    structured_property = (
        structured_item.get("project_name")
        or ""
    ).strip().lower()

    if (
        semantic_property
        and structured_property
        and semantic_property == structured_property
    ):
        return True

    return False


def _filter_semantic_results(
    semantic_results: list[dict[str, Any]],
    structured_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Remove semantic property documents that are already
    represented by structured SQL results.

    Category pages and press releases remain available as
    supporting evidence.
    """

    filtered = []

    for semantic_item in semantic_results:

        document_type = semantic_item.get(
            "document_type",
            "general",
        )

        if document_type == "property":

            duplicate = any(
                _is_same_property(
                    semantic_item,
                    structured_item,
                )
                for structured_item in structured_results
            )

            if duplicate:
                continue

        filtered.append(
            semantic_item
        )

    return filtered


def hybrid_search(
    db: Session,
    *,
    query: str,
    filters: dict[str, Any] | None = None,
    brand: str | None = None,
    country: str | None = None,
    city: str | None = None,
    property_type: str | None = None,
    limit: int = 5,
) -> dict[str, Any]:
    """
    Hybrid retrieval pipeline.

    Structured property records are always the primary source
    for property searches.

    Chroma provides semantic supporting evidence.

    Semantic documents are never presented as actual
    Property records.
    """

    filters = filters or {}

    # --------------------------------------------------------
    # Resolve filters.
    #
    # The API normally passes the complete "understood"
    # dictionary. Explicit keyword arguments remain supported
    # for compatibility.
    # --------------------------------------------------------

    brand = (
        brand
        if brand is not None
        else filters.get("brand")
    )

    country = (
        country
        if country is not None
        else filters.get("country")
    )

    city = (
        city
        if city is not None
        else filters.get("city")
    )

    property_type = (
        property_type
        if property_type is not None
        else filters.get("property_type")
    )

    min_price = filters.get("min_price")

    max_price = filters.get("max_price")

    bedrooms = filters.get("bedrooms")

    bathrooms = filters.get("bathrooms")

    property_type = normalize_property_type(
        property_type
    )

    bedrooms = filters.get("bedrooms")
    bathrooms = filters.get("bathrooms")

    min_price = filters.get("min_price")
    max_price = filters.get("max_price")

    min_area = filters.get("min_area")
    max_area = filters.get("max_area")

    listing_type = filters.get("listing_type")
    status = filters.get("status")


    intent = filters.get("intent")

    # --------------------------------------------------------
    # Structured search
    # --------------------------------------------------------
    if intent == "property_search":
        structured_objects = structured_search(
            db,
            brand=brand,
            country=(
                country
                if country is not None
                else filters.get("country")
            ),
            city=city,
            property_type=property_type,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            min_price=min_price,
            max_price=max_price,
            min_area=min_area,
            max_area=max_area,
            listing_type=listing_type,
            status=status,
            limit=limit,
        )
    else:
        structured_objects = []

    has_structured_filters = any(
        [
            brand,
            country,
            city,
            property_type,
            min_price is not None,
            max_price is not None,
            bedrooms is not None,
            bathrooms is not None,
            min_area,
            max_area,
            listing_type,
            status,
        ]
    )

    structured_results = [
        _property_to_dict(item)
        for item in structured_objects
    ]

    # --------------------------------------------------------
    # Semantic search
    # --------------------------------------------------------
    if intent == "property_search" and has_structured_filters:
        semantic_results = []
    else:
        semantic_filters = {
            key: value
            for key, value in {
                "document_type": (
                    "property"
                    if intent == "property_search"
                    else None
                ),
                "country": country,
                "city": city,
                "brand": brand,
                "property_type": (
                    normalize_property_type(property_type)
                    if property_type
                    else None
                ),
            }.items()
            if value
        }

        semantic_results = _chroma_results(
            query,
            n_results=limit,
            filters=semantic_filters,
        )



    # Remove semantic property duplicates while keeping
    # category / press release documents as supporting
    # evidence.
    semantic_results = _filter_semantic_results(
        semantic_results,
        structured_results,
    )

    # --------------------------------------------------------
    # Determine retrieval type
    # --------------------------------------------------------

    if structured_results:
        retrieval_type = "hybrid"

    elif semantic_results:
        retrieval_type = "semantic"

    else:
        retrieval_type = "none"

    return {
        "results": structured_results,
        "retrieval_type": retrieval_type,
        "count": len(structured_results),
        "semantic_results": semantic_results,
    }
