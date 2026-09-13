from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.property import Property


def _similarity_score(
    target: Property,
    comparable: Property,
) -> float:
    """
    Calculate a simple 0-100 similarity score.

    Higher means the comparable is more similar to the
    target property.
    """

    score = 0.0
    possible = 0.0

    # Property type
    if target.property_type and comparable.property_type:
        possible += 25

        if (
            target.property_type.strip().lower()
            == comparable.property_type.strip().lower()
        ):
            score += 25

    # City
    if target.city and comparable.city:
        possible += 20

        if (
            target.city.strip().lower()
            == comparable.city.strip().lower()
        ):
            score += 20

    # Bedrooms
    if (
        target.bedrooms is not None
        and comparable.bedrooms is not None
    ):
        possible += 20

        difference = abs(
            target.bedrooms
            - comparable.bedrooms
        )

        if difference == 0:
            score += 20
        elif difference == 1:
            score += 12

    # Area
    if (
        target.area is not None
        and comparable.area is not None
        and target.area > 0
    ):
        possible += 20

        area_difference = abs(
            comparable.area - target.area
        ) / target.area

        if area_difference <= 0.10:
            score += 20
        elif area_difference <= 0.25:
            score += 12
        elif area_difference <= 0.40:
            score += 6

    # Developer
    if target.developer and comparable.developer:
        possible += 15

        if (
            target.developer.strip().lower()
            == comparable.developer.strip().lower()
        ):
            score += 15

    if possible == 0:
        return 0.0

    return round(
        (score / possible) * 100,
        2,
    )


def find_comparables(
    db: Session,
    property_id: int,
    limit: int = 10,
) -> dict[str, Any]:
    """
    Find properties comparable to the target property.
    """

    target = (
        db.query(Property)
        .filter(Property.id == property_id)
        .first()
    )

    if not target:
        return {
            "property_id": property_id,
            "property_found": False,
            "comparables": [],
            "comparable_count": 0,
        }

    query = (
        db.query(Property)
        .filter(Property.id != property_id)
    )

    # Prefer properties in the same city.
    if target.city:
        query = query.filter(
            Property.city == target.city
        )

    # Prefer the same property type.
    if target.property_type:
        query = query.filter(
            Property.property_type
            == target.property_type
        )

    candidates = query.all()

    scored = []

    for comparable in candidates:
        similarity = _similarity_score(
            target,
            comparable,
        )

        if similarity <= 0:
            continue

        scored.append(
            {
                "property": comparable,
                "similarity_score": similarity,
            }
        )

    scored.sort(
        key=lambda item: item["similarity_score"],
        reverse=True,
    )

    selected = scored[:limit]

    results = []

    for item in selected:
        comparable = item["property"]

        results.append(
            {
                "id": comparable.id,
                "title": comparable.title,
                "project_name": comparable.project_name,
                "developer": comparable.developer,
                "property_type": comparable.property_type,
                "city": comparable.city,
                "location": comparable.location,
                "price": comparable.price,
                "currency": comparable.currency,
                "bedrooms": comparable.bedrooms,
                "bathrooms": comparable.bathrooms,
                "area": comparable.area,
                "area_unit": comparable.area_unit,
                "similarity_score": item[
                    "similarity_score"
                ],
                "source": comparable.source,
                "source_url": comparable.source_url,
            }
        )

    return {
        "property_id": property_id,
        "property_found": True,
        "target": {
            "id": target.id,
            "title": target.title,
            "project_name": target.project_name,
            "developer": target.developer,
            "property_type": target.property_type,
            "city": target.city,
            "price": target.price,
            "currency": target.currency,
            "bedrooms": target.bedrooms,
            "area": target.area,
            "area_unit": target.area_unit,
        },
        "comparables": results,
        "comparable_count": len(results),
    }


def calculate_comparable_metrics(
    comparable_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate simple market metrics from comparable properties.
    """

    comparables = comparable_result.get(
        "comparables",
        [],
    )

    priced = [
        item
        for item in comparables
        if item.get("price") is not None
        and item.get("price") > 0
    ]

    if not priced:
        return {
            "comparable_count": len(comparables),
            "priced_comparables": 0,
            "average_price": None,
            "median_price": None,
            "average_price_per_area": None,
        }

    prices = [
        item["price"]
        for item in priced
    ]

    prices_sorted = sorted(prices)

    average_price = (
        sum(prices)
        / len(prices)
    )

    middle = len(prices_sorted) // 2

    if len(prices_sorted) % 2 == 0:
        median_price = (
            prices_sorted[middle - 1]
            + prices_sorted[middle]
        ) / 2
    else:
        median_price = prices_sorted[middle]

    price_per_area = []

    for item in priced:
        area = item.get("area")

        if area and area > 0:
            price_per_area.append(
                item["price"] / area
            )

    average_price_per_area = None

    if price_per_area:
        average_price_per_area = (
            sum(price_per_area)
            / len(price_per_area)
        )

    return {
        "comparable_count": len(comparables),
        "priced_comparables": len(priced),
        "average_price": round(
            average_price,
            2,
        ),
        "median_price": round(
            median_price,
            2,
        ),
        "average_price_per_area": (
            round(
                average_price_per_area,
                2,
            )
            if average_price_per_area is not None
            else None
        ),
    }
