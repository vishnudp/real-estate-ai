from __future__ import annotations

from math import asin, cos, radians, sin, sqrt
from typing import Any

from sqlalchemy.orm import Session

from app.models.location import Location
from app.models.property import Property


EARTH_RADIUS_KM = 6371.0


def haversine_distance_km(
    latitude_1: float,
    longitude_1: float,
    latitude_2: float,
    longitude_2: float,
) -> float:
    """
    Calculate the great-circle distance between two
    geographic coordinates in kilometers.
    """

    lat1 = radians(latitude_1)
    lon1 = radians(longitude_1)

    lat2 = radians(latitude_2)
    lon2 = radians(longitude_2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * asin(sqrt(a))

    return EARTH_RADIUS_KM * c


def get_property_location(
    db: Session,
    property_id: int,
) -> Location | None:
    """
    Resolve the Location associated with a property.
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
        .filter(Location.id == property_item.location_id)
        .first()
    )


def calculate_distance_to_location(
    property_location: Location,
    target_location: Location,
) -> float | None:
    """
    Calculate distance between two Location records.
    """

    if (
        property_location.latitude is None
        or property_location.longitude is None
        or target_location.latitude is None
        or target_location.longitude is None
    ):
        return None

    return haversine_distance_km(
        property_location.latitude,
        property_location.longitude,
        target_location.latitude,
        target_location.longitude,
    )


def find_nearby_locations(
    db: Session,
    property_location: Location,
    *,
    location_type: str | None = None,
    radius_km: float = 50.0,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """
    Find nearby Location records within a radius.
    """

    if (
        property_location.latitude is None
        or property_location.longitude is None
    ):
        return []

    query = db.query(Location).filter(
        Location.id != property_location.id,
        Location.latitude.is_not(None),
        Location.longitude.is_not(None),
    )

    if location_type:
        query = query.filter(
            Location.location_type == location_type
        )

    locations = query.all()

    results = []

    for location in locations:
        distance = calculate_distance_to_location(
            property_location,
            location,
        )

        if distance is None:
            continue

        if distance > radius_km:
            continue

        results.append(
            {
                "id": location.id,
                "name": location.name,
                "location_type": location.location_type,
                "country": location.country,
                "city": location.city,
                "area": location.area,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "distance_km": round(distance, 2),
                "source": location.source,
                "source_url": location.source_url,
            }
        )

    results.sort(
        key=lambda item: item["distance_km"]
    )

    return results[:limit]


def analyze_property_location(
    db: Session,
    property_id: int,
) -> dict[str, Any]:
    """
    Produce the initial location intelligence result
    for a property.
    """

    location = get_property_location(
        db,
        property_id,
    )

    if not location:
        return {
            "property_id": property_id,
            "location_found": False,
            "location_score": None,
            "evidence": [],
            "confidence": 0.0,
        }

    nearby_airports = find_nearby_locations(
        db,
        location,
        location_type="airport",
        radius_km=100,
        limit=5,
    )

    nearby_developments = find_nearby_locations(
        db,
        location,
        location_type="development",
        radius_km=50,
        limit=5,
    )

    nearby_cities = find_nearby_locations(
        db,
        location,
        location_type="city",
        radius_km=100,
        limit=5,
    )

    evidence = []

    if nearby_airports:
        nearest_airport = nearby_airports[0]

        evidence.append(
            {
                "type": "airport_proximity",
                "name": nearest_airport["name"],
                "distance_km": nearest_airport["distance_km"],
                "source": nearest_airport["source"],
                "source_url": nearest_airport["source_url"],
            }
        )

    if nearby_cities:
        nearest_city = nearby_cities[0]

        evidence.append(
            {
                "type": "city_proximity",
                "name": nearest_city["name"],
                "distance_km": nearest_city["distance_km"],
                "source": nearest_city["source"],
                "source_url": nearest_city["source_url"],
            }
        )

    # Initial POC score.
    #
    # This is intentionally simple. We will replace this
    # with a proper weighted scoring model after adding
    # infrastructure and POI intelligence.
    location_score = 50.0

    if nearby_airports:
        airport_distance = nearby_airports[0]["distance_km"]

        if airport_distance <= 10:
            location_score += 20
        elif airport_distance <= 25:
            location_score += 15
        elif airport_distance <= 50:
            location_score += 10

    location_score = min(
        100.0,
        location_score,
    )

    return {
        "property_id": property_id,
        "location_found": True,
        "location": {
            "id": location.id,
            "name": location.name,
            "location_type": location.location_type,
            "country": location.country,
            "city": location.city,
            "area": location.area,
            "latitude": location.latitude,
            "longitude": location.longitude,
        },
        "nearby_airports": nearby_airports,
        "nearby_developments": nearby_developments,
        "nearby_cities": nearby_cities,
        "location_score": round(
            location_score,
            2,
        ),
        "evidence": evidence,
        "confidence": 0.80,
    }
    