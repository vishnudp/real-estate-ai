from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.infrastructure import Infrastructure
from app.models.location import Location
from app.models.property import Property
from app.services.location_engine import (
    haversine_distance_km,
)


# Maximum useful distance for each infrastructure category.
CATEGORY_RADII_KM = {
    "airport": 100.0,
    "hospital": 30.0,
    "school": 30.0,
    "shopping": 30.0,
    "road": 20.0,
    "tourism": 50.0,
}


# Maximum distance considered "excellent" for each category.
IDEAL_DISTANCE_KM = {
    "airport": 15.0,
    "hospital": 10.0,
    "school": 10.0,
    "shopping": 10.0,
    "road": 5.0,
    "tourism": 15.0,
}


CATEGORY_WEIGHTS = {
    "airport": 0.15,
    "hospital": 0.20,
    "school": 0.15,
    "shopping": 0.15,
    "road": 0.20,
    "tourism": 0.15,
}


def _distance_score(
    distance_km: float,
    ideal_distance_km: float,
    maximum_distance_km: float,
) -> float:
    """
    Convert distance into a 0-100 proximity score.

    Closer is better.
    """

    if distance_km <= ideal_distance_km:
        return 100.0

    if distance_km >= maximum_distance_km:
        return 0.0

    score = (
        1
        - (
            distance_km - ideal_distance_km
        )
        / (
            maximum_distance_km
            - ideal_distance_km
        )
    ) * 100

    return max(
        0.0,
        min(100.0, score),
    )


def _get_property_location(
    db: Session,
    property_id: int,
) -> Location | None:
    """
    Resolve the geographic Location associated with a property.
    """

    property_item = (
        db.query(Property)
        .filter(Property.id == property_id)
        .first()
    )

    if not property_item:
        return None

    if not property_item.location_id:
        return None

    return (
        db.query(Location)
        .filter(
            Location.id == property_item.location_id
        )
        .first()
    )


def _find_nearest(
    db: Session,
    property_location: Location,
    infrastructure_type: str,
) -> dict[str, Any] | None:
    """
    Find the nearest infrastructure item of a specific type.
    """

    if (
        property_location.latitude is None
        or property_location.longitude is None
    ):
        return None

    infrastructure_items = (
        db.query(Infrastructure)
        .filter(
            Infrastructure.infrastructure_type
            == infrastructure_type,
            Infrastructure.latitude.is_not(None),
            Infrastructure.longitude.is_not(None),
        )
        .all()
    )

    nearest = None
    nearest_distance = None

    for item in infrastructure_items:

        distance = haversine_distance_km(
            property_location.latitude,
            property_location.longitude,
            item.latitude,
            item.longitude,
        )

        if (
            nearest_distance is None
            or distance < nearest_distance
        ):
            nearest = item
            nearest_distance = distance

    if nearest is None:
        return None

    return {
        "id": nearest.id,
        "name": nearest.name,
        "type": nearest.infrastructure_type,
        "city": nearest.city,
        "area": nearest.area,
        "distance_km": round(
            nearest_distance,
            2,
        ),
        "importance": nearest.importance,
        "source": nearest.source,
        "source_url": nearest.source_url,
    }


def analyze_property_infrastructure(
    db: Session,
    property_id: int,
) -> dict[str, Any]:
    """
    Analyze infrastructure surrounding a property.

    Returns:
    - nearest infrastructure by category
    - category scores
    - weighted infrastructure score
    - evidence
    - confidence
    """

    location = _get_property_location(
        db,
        property_id,
    )

    if not location:
        return {
            "property_id": property_id,
            "location_found": False,
            "infrastructure_score": None,
            "categories": {},
            "evidence": [],
            "confidence": 0.0,
        }

    if (
        location.latitude is None
        or location.longitude is None
    ):
        return {
            "property_id": property_id,
            "location_found": True,
            "coordinates_available": False,
            "infrastructure_score": None,
            "categories": {},
            "evidence": [],
            "confidence": 0.0,
        }

    categories = {}
    evidence = []

    weighted_score = 0.0
    total_weight = 0.0

    for infrastructure_type, weight in CATEGORY_WEIGHTS.items():

        nearest = _find_nearest(
            db,
            location,
            infrastructure_type,
        )

        if nearest is None:
            continue

        maximum_distance = CATEGORY_RADII_KM[
            infrastructure_type
        ]

        ideal_distance = IDEAL_DISTANCE_KM[
            infrastructure_type
        ]

        score = _distance_score(
            nearest["distance_km"],
            ideal_distance,
            maximum_distance,
        )

        categories[infrastructure_type] = {
            "nearest": nearest,
            "score": round(
                score,
                2,
            ),
            "weight": weight,
        }

        weighted_score += score * weight
        total_weight += weight

        evidence.append(
            {
                "type": infrastructure_type,
                "name": nearest["name"],
                "distance_km": nearest["distance_km"],
                "score": round(score, 2),
                "source": nearest["source"],
                "source_url": nearest["source_url"],
            }
        )

    if total_weight == 0:
        infrastructure_score = None
        confidence = 0.0
    else:
        infrastructure_score = (
            weighted_score / total_weight
        )

        # Confidence increases with category coverage.
        confidence = min(
            1.0,
            total_weight / 1.0,
        )

    return {
        "property_id": property_id,
        "location_found": True,
        "coordinates_available": True,
        "location": {
            "id": location.id,
            "name": location.name,
            "city": location.city,
            "country": location.country,
            "latitude": location.latitude,
            "longitude": location.longitude,
        },
        "categories": categories,
        "infrastructure_score": (
            round(
                infrastructure_score,
                2,
            )
            if infrastructure_score is not None
            else None
        ),
        "evidence": evidence,
        "confidence": round(
            confidence,
            2,
        ),
    }
