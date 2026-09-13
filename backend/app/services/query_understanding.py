import re


COUNTRIES = {
    "oman": "Oman",
    "maldives": "Maldives",
    "france": "France",
    "spain": "Spain",
    "qatar": "Qatar",
    "saudi arabia": "Saudi Arabia",
    "saudi": "Saudi Arabia",
    "united arab emirates": "United Arab Emirates",
    "uae": "United Arab Emirates",
    "united kingdom": "United Kingdom",
    "uk": "United Kingdom",
}



CITIES = {
    "muscat": "Muscat",
    "dubai": "Dubai",
    "abu dhabi": "Abu Dhabi",
    "doha": "Doha",
    "jeddah": "Jeddah",
    "riyadh": "Riyadh",
    "london": "London",
}


BRANDS = {
    "marriott": "Marriott",
    "trump": "Trump",
    "missoni": "Missoni",
    "pagani": "Pagani",
    "mouawad": "Mouawad",
}


# Canonical property types used by the database.
PROPERTY_TYPES = {
    "hotel residences": "hotel_residences",
    "hotel residence": "hotel_residences",
    "branded residences": "hotel_residences",
    "branded residence": "hotel_residences",
    "residences": "hotel_residences",
    "residence": "hotel_residences",

    "apartments": "apartments",
    "apartment": "apartments",

    "villas": "villas",
    "villa": "villas",

    "hotel & resort": "hotel_resort",
    "hotel and resort": "hotel_resort",
    "hotel resort": "hotel_resort",
    "resort": "hotel_resort",
}


def find_value(
    text: str,
    values: dict[str, str],
) -> str | None:
    """
    Find the first matching value.

    Longer phrases are checked first so that:

        hotel residences

    is detected before:

        residences
    """

    text_lower = text.lower()

    for marker in sorted(
        values,
        key=len,
        reverse=True,
    ):
        if re.search(
            rf"\b{re.escape(marker)}\b",
            text_lower,
        ):
            return values[marker]

    return None

def extract_number(
    text: str,
    pattern: str,
) -> float | None:
    match = re.search(pattern, text.lower())

    if not match:
        return None

    try:
        return float(
            match.group(1).replace(",", "")
        )
    except (ValueError, AttributeError):
        return None


def extract_max_price(
    text: str,
) -> float | None:
    patterns = [
        r"(?:under|below|less than|up to)\s*\$?\s*([\d,]+(?:\.\d+)?)\s*(million|m|k)?",
        r"\$?\s*([\d,]+(?:\.\d+)?)\s*(million|m|k)?\s*(?:or less|maximum|max)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text.lower(),
        )

        if not match:
            continue

        try:
            value = float(
                match.group(1).replace(",", "")
            )

            unit = match.group(2)

            if unit in ("million", "m"):
                value *= 1_000_000
            elif unit == "k":
                value *= 1_000

            return value

        except (ValueError, AttributeError):
            continue

    return None


def extract_min_price(
    text: str,
) -> float | None:
    patterns = [
        r"(?:over|above|more than|from)\s*\$?\s*([\d,]+(?:\.\d+)?)\s*(million|m|k)?",
        r"\$?\s*([\d,]+(?:\.\d+)?)\s*(million|m|k)?\s*(?:or more|minimum|min)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text.lower(),
        )

        if not match:
            continue

        try:
            value = float(
                match.group(1).replace(",", "")
            )

            unit = match.group(2)

            if unit in ("million", "m"):
                value *= 1_000_000
            elif unit == "k":
                value *= 1_000

            return value

        except (ValueError, AttributeError):
            continue

    return None


def extract_bedrooms(
    text: str,
) -> int | None:
    match = re.search(
        r"(\d+)\s*(?:bedroom|bedrooms|br)\b",
        text.lower(),
    )

    if not match:
        return None

    return int(match.group(1))


def extract_bathrooms(
    text: str,
) -> int | None:
    match = re.search(
        r"(\d+)\s*(?:bathroom|bathrooms|bath|baths)\b",
        text.lower(),
    )

    if not match:
        return None

    return int(match.group(1))



def detect_intent(query: str) -> str:
    text = query.lower()

    # --------------------------------------------------------
    # INVESTMENT ANALYSIS
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "good investment",
            "good buy",
            "worth buying",
            "worth it",
            "should i buy",
            "should i invest",
            "investment",
            "investing",
            "investor",
            "investment potential",
            "investment opportunity",
            "profitable",
            "profit potential",
            "return on investment",
            "roi",
        ]
    ):
        return "investment_analysis"

    # --------------------------------------------------------
    # GENERAL / KNOWLEDGE QUESTIONS
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "what is",
            "what are",
            "tell me about",
            "explain",
            "requirements",
            "requirement",
            "eligibility",
            "eligible",
            "how does",
            "how do i",
            "golden visa",
            "visa requirements",
        ]
    ):
        return "general"

    # --------------------------------------------------------
    # VALUATION
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "valuation",
            "fair value",
            "value of",
            "how much is",
            "what is it worth",
        ]
    ):
        return "valuation"

    # --------------------------------------------------------
    # COMPARABLES
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "compare",
            "comparison",
            "comparable",
            "similar",
        ]
    ):
        return "comparables"

    # --------------------------------------------------------
    # LOCATION INTELLIGENCE
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "location",
            "near",
            "nearby",
            "schools",
            "hospital",
            "airport",
            "metro",
        ]
    ):
        return "location_intelligence"

    # --------------------------------------------------------
    # PROPERTY SEARCH
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "available",
            "properties",
            "property",
            "residences",
            "residence",
            "apartments",
            "apartment",
            "villas",
            "villa",
            "listings",
            "show me",
            "find me",
        ]
    ):
        return "property_search"

    return "general"




def understand_query(query: str) -> dict:
    """
    Convert a natural-language query into canonical filters.
    """

    query = query.strip()

    return {
        "query": query,

        "intent": detect_intent(query),

        "brand": find_value(
            query,
            BRANDS,
        ),

        "country": find_value(
            query,
            COUNTRIES,
        ),

        "city": find_value(
            query,
            CITIES,
        ),

        "property_type": find_value(
            query,
            PROPERTY_TYPES,
        ),

        "min_price": extract_min_price(
            query
        ),

        "max_price": extract_max_price(
            query
        ),

        "bedrooms": extract_bedrooms(
            query
        ),

        "bathrooms": extract_bathrooms(
            query
        ),
    }

