import re
from typing import Any


INTENT_PROPERTY_SEARCH = "property_search"
INTENT_UNKNOWN = "unknown"


KNOWN_BRANDS = [
    "Marriott",
    "Trump",
    "Missoni",
    "Pagani",
    "Mouawad",
]


KNOWN_COUNTRIES = [
    "Oman",
    "Maldives",
    "United Arab Emirates",
    "UAE",
    "Saudi Arabia",
    "Qatar",
    "United Kingdom",
    "UK",
]


KNOWN_CITIES = [
    "Muscat",
    "Dubai",
    "Abu Dhabi",
    "Doha",
    "Jeddah",
    "Riyadh",
    "London",
]


KNOWN_PROPERTY_TYPES = {
    "hotel residences": "hotel_residences",
    "hotel residence": "hotel_residences",
    "residences": "residences",
    "residential": "residential",
    "apartments": "apartments",
    "apartment": "apartments",
    "villas": "villas",
    "villa": "villas",
    "hotel resort": "hotel_resort",
    "resort": "hotel_resort",
}


SEARCH_TERMS = [
    "property",
    "properties",
    "project",
    "projects",
    "residence",
    "residences",
    "residential",
    "apartment",
    "apartments",
    "villa",
    "villas",
    "hotel",
    "resort",
    "real estate",
    "available",
    "available in",
    "for sale",
    "buy",
    "price",
    "bedroom",
    "bedrooms",
]


def _contains(text: str, value: str) -> bool:
    return value.lower() in text.lower()


def _extract_brand(text: str) -> str | None:
    for brand in KNOWN_BRANDS:
        if _contains(text, brand):
            return brand

    return None


def _extract_country(text: str) -> str | None:
    for country in KNOWN_COUNTRIES:
        if _contains(text, country):
            if country == "UAE":
                return "United Arab Emirates"

            if country == "UK":
                return "United Kingdom"

            return country

    return None


def _extract_city(text: str) -> str | None:
    for city in KNOWN_CITIES:
        if _contains(text, city):
            return city

    return None


def _extract_property_type(text: str) -> str | None:
    text_lower = text.lower()

    # More specific types first.
    if "hotel residences" in text_lower:
        return "hotel_residences"

    if "hotel residence" in text_lower:
        return "hotel_residences"

    for marker, property_type in KNOWN_PROPERTY_TYPES.items():
        if marker in text_lower:
            return property_type

    return None


def _looks_like_property_query(text: str) -> bool:
    text_lower = text.lower()

    return any(
        term in text_lower
        for term in SEARCH_TERMS
    )


def understand_query(query: str) -> dict[str, Any]:
    """
    Convert a natural-language property question into
    structured search criteria.

    This is intentionally deterministic for the first
    implementation. We can replace/extend this with an
    LLM-based query understanding layer later.
    """

    query = (query or "").strip()

    if not query:
        return {
            "intent": INTENT_UNKNOWN,
            "query": "",
            "brand": None,
            "country": None,
            "city": None,
            "property_type": None,
        }

    brand = _extract_brand(query)
    country = _extract_country(query)
    city = _extract_city(query)
    property_type = _extract_property_type(query)

    is_property_query = _looks_like_property_query(query)

    # Entity signals can also make a query meaningful even
    # when the user did not explicitly say "property".
    if brand or country or city or property_type:
        is_property_query = True

    return {
        "intent": (
            INTENT_PROPERTY_SEARCH
            if is_property_query
            else INTENT_UNKNOWN
        ),
        "query": query,
        "brand": brand,
        "country": country,
        "city": city,
        "property_type": property_type,
    }
