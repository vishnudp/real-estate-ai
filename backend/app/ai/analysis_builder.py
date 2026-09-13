from __future__ import annotations

from typing import Any


def _format_price(
    price: float | int | None,
    currency: str | None,
) -> str | None:
    if price is None:
        return None

    currency_symbol = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "AED": "AED ",
        "OMR": "OMR ",
        "SAR": "SAR ",
    }.get(
        currency or "",
        f"{currency} " if currency else "",
    )

    return f"{currency_symbol}{price:,.2f}"


def _infrastructure_assessment(
    score: float | None,
) -> str:
    if score is None:
        return "unknown"

    if score >= 80:
        return "strong"

    if score >= 60:
        return "moderate"

    if score >= 40:
        return "weak"

    return "poor"


def _get_category_score(
    infrastructure_data: dict[str, Any],
    category: str,
) -> float | None:
    categories = infrastructure_data.get(
        "categories",
        {},
    )

    category_data = categories.get(
        category,
        {},
    )

    score = category_data.get("score")

    if score is None:
        return None

    try:
        return float(score)
    except (TypeError, ValueError):
        return None


def _build_infrastructure_intelligence(
    infrastructure_data: dict[str, Any],
) -> dict[str, Any]:
    raw_score = infrastructure_data.get(
        "infrastructure_score"
    )

    score = None

    if raw_score is not None:
        try:
            score = float(raw_score)
        except (TypeError, ValueError):
            score = None

    assessment = _infrastructure_assessment(
        score
    )

    categories = {
        "airport": "Airport accessibility",
        "hospital": "Healthcare accessibility",
        "school": "Education accessibility",
        "shopping": "Shopping accessibility",
        "road": "Road connectivity",
        "tourism": "Tourism accessibility",
    }

    strengths: list[str] = []
    weaknesses: list[str] = []

    category_scores: dict[str, float] = {}

    for category, label in categories.items():
        category_score = _get_category_score(
            infrastructure_data,
            category,
        )

        if category_score is None:
            continue

        category_scores[category] = category_score

        if category_score >= 75:
            strengths.append(
                f"Strong {label.lower()}"
            )

        elif category_score < 50:
            weaknesses.append(
                f"Weaker {label.lower()}"
            )

    return {
        "score": score,
        "assessment": assessment,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "category_scores": category_scores,
    }


def _build_pricing_intelligence(
    property_data: dict[str, Any],
    comparable_data: dict[str, Any],
    comparable_metrics: dict[str, Any],
) -> dict[str, Any]:
    target_price = property_data.get(
        "price"
    )

    target_currency = property_data.get(
        "currency"
    )

    target_area = property_data.get(
        "area"
    )

    comparable_items = comparable_data.get(
        "comparables",
        [],
    )

    priced_comparables = [
        item
        for item in comparable_items
        if item.get("price") is not None
    ]

    comparable_prices = [
        float(item["price"])
        for item in priced_comparables
        if isinstance(
            item.get("price"),
            (int, float),
        )
    ]

    price_range = None

    if comparable_prices:
        price_range = {
            "min": min(comparable_prices),
            "max": max(comparable_prices),
        }

    target_price_available = (
        target_price is not None
    )

    target_area_available = (
        target_area is not None
    )

    comparable_currency = None

    if priced_comparables:
        comparable_currency = (
            priced_comparables[0].get(
                "currency"
            )
        )

    return {
        "available": bool(
            priced_comparables
        ),
        "target_price_available": (
            target_price_available
        ),
        "target_area_available": (
            target_area_available
        ),
        "target_price": target_price,
        "target_currency": target_currency,
        "target_price_formatted": _format_price(
            target_price,
            target_currency,
        ),
        "comparable_count": (
            comparable_metrics.get(
                "comparable_count",
                0,
            )
        ),
        "priced_comparables": (
            comparable_metrics.get(
                "priced_comparables",
                len(priced_comparables),
            )
        ),
        "average_price": (
            comparable_metrics.get(
                "average_price"
            )
        ),
        "median_price": (
            comparable_metrics.get(
                "median_price"
            )
        ),
        "average_price_per_area": (
            comparable_metrics.get(
                "average_price_per_area"
            )
        ),
        "price_range": price_range,
        "currency": (
            comparable_currency
            or target_currency
        ),
    }


def _calculate_data_completeness(
    property_data: dict[str, Any],
    infrastructure_data: dict[str, Any],
    comparable_metrics: dict[str, Any],
) -> float:
    fields = [
        property_data.get("project_name"),
        property_data.get("developer"),
        property_data.get("property_type"),
        property_data.get("country"),
        property_data.get("city"),
        property_data.get("location"),
        property_data.get("price"),
        property_data.get("bedrooms"),
        property_data.get("bathrooms"),
        property_data.get("area"),
        property_data.get("description"),
        property_data.get("brands"),
    ]

    available_fields = sum(
        value is not None
        and value != ""
        and value != []
        for value in fields
    )

    property_completeness = (
        available_fields
        / len(fields)
    )

    infrastructure_available = (
        infrastructure_data.get(
            "location_found",
            False,
        )
        and infrastructure_data.get(
            "coordinates_available",
            False,
        )
    )

    comparable_available = (
        comparable_metrics.get(
            "comparable_count",
            0,
        )
        > 0
    )

    infrastructure_score = (
        1.0
        if infrastructure_available
        else 0.0
    )

    comparable_score = (
        1.0
        if comparable_available
        else 0.0
    )

    completeness = (
        property_completeness * 0.6
        + infrastructure_score * 0.2
        + comparable_score * 0.2
    )

    return round(
        completeness,
        2,
    )


def _calculate_confidence(
    infrastructure_data: dict[str, Any],
    comparable_metrics: dict[str, Any],
) -> float:
    infrastructure_confidence = float(
        infrastructure_data.get(
            "confidence",
            0.0,
        )
        or 0.0
    )

    comparable_count = comparable_metrics.get(
        "comparable_count",
        0,
    )

    if comparable_count >= 5:
        comparable_confidence = 1.0

    elif comparable_count >= 3:
        comparable_confidence = 0.8

    elif comparable_count >= 1:
        comparable_confidence = 0.5

    else:
        comparable_confidence = 0.0

    confidence = (
        infrastructure_confidence * 0.5
        + comparable_confidence * 0.5
    )

    return round(
        confidence,
        2,
    )


def _build_strengths(
    infrastructure: dict[str, Any],
    pricing: dict[str, Any],
) -> list[str]:
    strengths = list(
        infrastructure.get(
            "strengths",
            [],
        )
    )

    score = infrastructure.get(
        "score"
    )

    if score is not None:
        if score >= 80:
            strengths.append(
                "Strong overall infrastructure profile"
            )

        elif score >= 60:
            strengths.append(
                "Moderate overall infrastructure profile"
            )

    if pricing.get("available"):
        strengths.append(
            "Comparable market pricing is available"
        )

    if pricing.get(
        "comparable_count",
        0,
    ) >= 3:
        strengths.append(
            "Multiple comparable properties support "
            "the market view"
        )

    return strengths


def _build_risks(
    property_data: dict[str, Any],
    infrastructure: dict[str, Any],
    pricing: dict[str, Any],
) -> list[str]:
    risks = list(
        infrastructure.get(
            "weaknesses",
            [],
        )
    )

    if not pricing.get(
        "target_price_available",
        False,
    ):
        risks.append(
            "Target property price is unavailable"
        )

    if not pricing.get(
        "target_area_available",
        False,
    ):
        risks.append(
            "Target property area is unavailable"
        )

    if pricing.get(
        "comparable_count",
        0,
    ) == 0:
        risks.append(
            "Insufficient comparable market data"
        )

    if not property_data.get(
        "bedrooms"
    ):
        risks.append(
            "Bedroom configuration is unavailable"
        )

    return risks


def _build_assessment(
    infrastructure_score: float | None,
    pricing: dict[str, Any],
    data_completeness: float,
) -> str:
    positive_factors = 0
    negative_factors = 0

    if (
        infrastructure_score is not None
        and infrastructure_score >= 60
    ):
        positive_factors += 1

    if pricing.get(
        "comparable_count",
        0,
    ) >= 3:
        positive_factors += 1

    if pricing.get(
        "target_price_available",
        False,
    ):
        positive_factors += 1
    else:
        negative_factors += 1

    if pricing.get(
        "target_area_available",
        False,
    ):
        positive_factors += 1
    else:
        negative_factors += 1

    if data_completeness < 0.5:
        negative_factors += 1

    if (
        positive_factors >= 3
        and negative_factors <= 1
    ):
        return "attractive"

    if positive_factors >= 2:
        return "moderately_attractive"

    if negative_factors >= 3:
        return "high_uncertainty"

    return "neutral"


def build_property_intelligence(
    property_data: dict[str, Any],
    infrastructure_data: dict[str, Any],
    comparable_data: dict[str, Any],
    comparable_metrics: dict[str, Any],
) -> dict[str, Any]:
    infrastructure = (
        _build_infrastructure_intelligence(
            infrastructure_data
        )
    )

    pricing = _build_pricing_intelligence(
        property_data=property_data,
        comparable_data=comparable_data,
        comparable_metrics=comparable_metrics,
    )

    data_completeness = (
        _calculate_data_completeness(
            property_data=property_data,
            infrastructure_data=infrastructure_data,
            comparable_metrics=comparable_metrics,
        )
    )

    confidence = _calculate_confidence(
        infrastructure_data=infrastructure_data,
        comparable_metrics=comparable_metrics,
    )

    strengths = _build_strengths(
        infrastructure=infrastructure,
        pricing=pricing,
    )

    risks = _build_risks(
        property_data=property_data,
        infrastructure=infrastructure,
        pricing=pricing,
    )

    assessment = _build_assessment(
        infrastructure_score=(
            infrastructure.get("score")
        ),
        pricing=pricing,
        data_completeness=data_completeness,
    )

    project_name = (
        property_data.get("project_name")
        or property_data.get("title")
        or "This property"
    )

    location_parts = [
        property_data.get("location"),
        property_data.get("city"),
        property_data.get("country"),
    ]

    location = ", ".join(
        str(part)
        for part in location_parts
        if part
    )

    developer = property_data.get(
        "developer"
    )

    if location:
        summary = (
            f"{project_name} is located in "
            f"{location}"
        )
    else:
        summary = (
            f"{project_name} is available"
        )

    if developer:
        summary += (
            f" and is developed by "
            f"{developer}"
        )

    infrastructure_score = (
        infrastructure.get("score")
    )

    if infrastructure_score is not None:
        summary += (
            f". Its infrastructure score is "
            f"{infrastructure_score:.2f}/100"
        )

    median_price = pricing.get(
        "median_price"
    )

    if median_price is not None:
        formatted_median = _format_price(
            median_price,
            pricing.get("currency"),
        )

        if formatted_median:
            summary += (
                f". The median comparable price is "
                f"{formatted_median}"
            )

    summary += "."

    return {
        "summary": summary,
        "assessment": assessment,
        "strengths": strengths,
        "risks": risks,
        "infrastructure": infrastructure,
        "pricing": pricing,
        "data_completeness": data_completeness,
        "confidence": confidence,
    }
