import re
from typing import Any, Dict, Optional


# ============================================================
# BLOCKED / BOT-PROTECTION DETECTION
# ============================================================

BLOCKED_MARKERS = [
    "just a moment",
    "performing security verification",
    "checking your browser",
    "verify you are human",
    "cloudflare",
    "security verification",
]


def is_blocked_page(record: Dict[str, Any]) -> bool:
    title = str(record.get("title", "")).lower()
    content = str(record.get("content", "")).lower()

    combined = f"{title} {content}"

    return any(
        marker in combined
        for marker in BLOCKED_MARKERS
    )


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text: Optional[str]) -> str:
    if not text:
        return ""

    text = str(text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove spaces before punctuation
    text = re.sub(r"\s+([,.!?])", r"\1", text)

    return text.strip()

# ============================================================
# PROPERTY METADATA EXTRACTION
# ============================================================

def extract_property_name(
    record: Dict[str, Any],
) -> Optional[str]:
    """
    Extract the individual property/project name.
    """

    title = clean_text(record.get("title"))

    if not title:
        return None

    # Known DarGlobal projects
    known_names = [
        "Marriott Residences Oman",
        "Trump International Hotel & Resort Maldives",
        "Trump International Resort Maldives",
    ]

    title_lower = title.lower()

    for name in known_names:
        if name.lower() in title_lower:
            return name

    # Remove common website suffixes
    name = re.sub(
        r"\s*\|\s*DarGlobal.*$",
        "",
        title,
        flags=re.IGNORECASE,
    )

    return name.strip() or None


def extract_developer(
    record: Dict[str, Any],
) -> Optional[str]:
    """
    Extract the developer from the page content.
    """

    text = " ".join(
        [
            clean_text(record.get("title")),
            clean_text(record.get("description")),
            clean_text(record.get("content")),
        ]
    )

    developer_markers = [
        "developed by DarGlobal",
        "DarGlobal development",
        "DarGlobal's",
        "DarGlobal on",
        "DarGlobal and",
    ]

    for marker in developer_markers:
        if marker.lower() in text.lower():
            return "DarGlobal"

    # Fallback for known DarGlobal source
    source_url = str(
        record.get("source_url", "")
    ).lower()

    if "darglobal.co.uk" in source_url:
        return "DarGlobal"

    return None


def extract_brand(
    record: Dict[str, Any],
) -> Optional[str]:
    """
    Extract the primary brand from the property's
    title and description.

    Do NOT search the entire page content because
    DarGlobal pages contain navigation and project
    selectors mentioning many unrelated brands.
    """

    text = " ".join(
        [
            clean_text(record.get("title")),
            clean_text(record.get("description")),
        ]
    ).lower()

    # Strongest / most specific signals first
    if "marriott" in text:
        return "Marriott"

    if "trump international" in text:
        return "Trump"

    if "trump" in text:
        return "Trump"

    if "missoni" in text:
        return "Missoni"

    if "pagani" in text:
        return "Pagani"

    if "mouawad" in text:
        return "Mouawad"

    return None


def extract_country(
    record: Dict[str, Any],
) -> Optional[str]:
    """
    Extract the property's country using the title
    and description.

    Avoid the full page content because global project
    selectors may contain many countries.
    """

    text = " ".join(
        [
            clean_text(record.get("title")),
            clean_text(record.get("description")),
        ]
    ).lower()

    countries = [
        ("oman", "Oman"),
        ("maldives", "Maldives"),
        ("united arab emirates", "United Arab Emirates"),
        ("uae", "United Arab Emirates"),
        ("saudi arabia", "Saudi Arabia"),
        ("qatar", "Qatar"),
        ("united kingdom", "United Kingdom"),
        ("uk", "United Kingdom"),
    ]

    for marker, country in countries:
        if marker in text:
            return country

    return None


def extract_city(
    record: Dict[str, Any],
) -> Optional[str]:
    text = " ".join(
        [
            clean_text(record.get("title")),
            clean_text(record.get("description")),
        ]
    )

    text_lower = text.lower()

    city_markers = [
        ("muscat", "Muscat"),
        ("doha", "Doha"),
        ("dubai", "Dubai"),
        ("abu dhabi", "Abu Dhabi"),
        ("jeddah", "Jeddah"),
        ("riyadh", "Riyadh"),
        ("london", "London"),
    ]

    for marker, city in city_markers:
        if marker in text_lower:
            return city

    return None



def extract_location(
    record: Dict[str, Any],
) -> Optional[str]:
    """
    Extract the property's primary named location.

    Prefer title/description over full page content.
    """

    text = " ".join(
        [
            clean_text(record.get("title")),
            clean_text(record.get("description")),
        ]
    )

    text_lower = text.lower()

    location_markers = [
        ("aida", "AIDA"),
        ("noonu atoll", "Noonu Atoll"),
        ("wadi safar", "Wadi Safar"),
        ("amaya", "Amaya"),
        ("rayana", "Rayana"),
    ]

    for marker, location in location_markers:
        if marker in text_lower:
            return location

    return None



def extract_property_type(
    record: Dict[str, Any],
) -> Optional[str]:
    """
    Determine the primary property type using only
    the property's title and description.

    More specific property types are checked before
    generic types to avoid classifications such as
    "hotel_residences" becoming "residences".
    """

    title = clean_text(
        record.get("title")
    )

    description = clean_text(
        record.get("description")
    )

    text = f"{title} {description}".lower()

    # Strong, property-specific signals first.
    if (
        "hotel residences" in text
        or "marriott residences" in text
    ):
        return "hotel_residences"

    

    if (
        "hotel & resort" in text
        or "hotel and resort" in text
    ):
        return "hotel_resort"

    if "branded residences" in text:
        return "branded_residences"

    if "private island" in text:
        return "private_island"

    if "lagoon villas" in text:
        return "villas"

    if "villas" in text:
        return "villas"

    if "villa" in text:
        return "villa"

    if "residences" in text:
        return "residences"

    if "residence" in text:
        return "residence"

    if "apartments" in text:
        return "apartments"

    if "apartment" in text:
        return "apartment"

    if "mansions" in text:
        return "mansions"

    if "mansion" in text:
        return "mansion"

    if "penthouse" in text:
        return "penthouse"

    if "townhouses" in text:
        return "townhouses"

    if "townhouse" in text:
        return "townhouse"

    return None




def extract_investment(
    record: Dict[str, Any],
) -> Optional[str]:
    """
    Extract investment-related information.

    This intentionally preserves the relevant text rather than
    interpreting investment claims numerically.
    """

    content = clean_text(
        record.get("content")
    )

    if not content:
        return None

    investment_markers = [
        "Reasons to Invest",
        "investment opportunities",
        "investment",
        "rental yield",
        "rental income",
        "revenue",
        "return",
    ]

    content_lower = content.lower()

    for marker in investment_markers:
        if marker.lower() in content_lower:
            # Capture a useful section around the first match.
            index = content_lower.find(
                marker.lower()
            )

            start = max(
                0,
                index - 100,
            )

            end = min(
                len(content),
                index + 1500,
            )

            return content[start:end].strip()

    return None


def extract_investment_type(
    record: Dict[str, Any],
) -> Optional[str]:
    """
    Classify the investment model mentioned on the page.

    Use title, description, and content, but keep the classification
    based on explicit investment/ownership language.
    """

    text = " ".join(
        [
            clean_text(record.get("title")),
            clean_text(record.get("description")),
            clean_text(record.get("content")),
        ]
    ).lower()

    if not text:
        return None

    if (
        "private ownership" in text
        or "home ownership" in text
        or "private home ownership" in text
    ):
        return "private_ownership"

    if (
        "rental yield" in text
        or "rental income" in text
    ):
        return "rental_income"

    if (
        "investment opportunities" in text
        or "investment" in text
        or "invest" in text
    ):
        return "investment"

    return None



# ============================================================
# NEWS / ARTICLE DETECTION
# ============================================================

def is_news_page(record: Dict[str, Any]) -> bool:
    """
    Detect press releases, news, blogs and articles.
    """

    url = str(
        record.get("source_url", "")
    ).lower()

    title = str(
        record.get("title", "")
    ).lower()

    news_url_markers = [
        "/press/",
        "/news/",
        "/blog/",
        "/insights/",
    ]

    news_title_markers = [
        "appoints",
        "announces",
        "announcement",
        "contract",
        "successfully executes",
        "marks",
        "awards",
        "launches",
    ]

    if any(
        marker in url
        for marker in news_url_markers
    ):
        return True

    if any(
        marker in title
        for marker in news_title_markers
    ):
        return True

    return False

def is_category_page(record: Dict[str, Any]) -> bool:
    """
    Detect DarGlobal category/listing pages.

    Category pages describe groups of properties and should not be
    treated as individual property/project records.
    """

    url = str(
        record.get("source_url", "")
    ).lower()

    category_url_markers = [
        "/projects/properties-in-",
        "/projects/properties/",
        "/properties-in-",
    ]

    if any(
        marker in url
        for marker in category_url_markers
    ):
        return True

    title = clean_text(
        record.get("title")
    ).lower()

    category_title_markers = [
        "properties in ",
        "apartments in ",
        "villas in ",
        "townhouses in ",
        "penthouses in ",
        "properties for sale",
        "properties for rent",
    ]

    if any(
        marker in title
        for marker in category_title_markers
    ):
        return True

    return False

def is_property_record(
    record: Dict[str, Any],
) -> bool:
    """
    Return True only for records representing an
    individual property/project.

    Category pages and news/press pages are knowledge
    documents and must not be stored as Property rows.
    """

    if is_category_page(record):
        return False

    if is_news_page(record):
        return False

    property_name = (
        record.get("property_name")
        or record.get("project_name")
    )

    if not property_name:
        return False

    return True

# ============================================================
# PROPERTY PAGE DETECTION
# ============================================================

def is_property_page(record: Dict[str, Any]) -> bool:
    """
    Detect an individual property/project page.

    Important:
    Category pages such as /projects/properties-in-oman
    are explicitly excluded.

    Press/news/article pages are also excluded.
    """

    url = str(
        record.get("source_url", "")
    ).lower()

    title = str(
        record.get("title", "")
    ).lower()

    # --------------------------------------------------------
    # 1. Category pages are NOT individual properties
    # --------------------------------------------------------

    if is_category_page(record):
        return False

    # --------------------------------------------------------
    # 2. News / press / articles are NOT properties
    # --------------------------------------------------------

    excluded_url_markers = [
        "/press/",
        "/news/",
        "/blog/",
        "/insights/",
        "/careers/",
        "/investor-relations/",
    ]

    if any(
        marker in url
        for marker in excluded_url_markers
    ):
        return False

    # --------------------------------------------------------
    # 3. Explicit individual property URL patterns
    # --------------------------------------------------------

    property_url_markers = [
        "/property/",
        "/property-detail/",
        "/project-detail/",
        "/development/",
        "/development-detail/",
        "/residence/",
        "/residences/",
        "/villa/",
        "/villas/",
        "/apartment/",
        "/apartments/",
        "/community/",
        "/communities/",
        "/partners/",
    ]

    if any(
        marker in url
        for marker in property_url_markers
    ):
        return True

    # --------------------------------------------------------
    # 4. Known DarGlobal project-style pages
    #
    # Some DarGlobal project pages do not have a standard
    # /property/ URL.
    # --------------------------------------------------------

    known_project_markers = [
        "trump-international-resort",
        "marriott-residences",
        "trump-international-hotel",
        "trump-cliff-villas",
        "trump-golf-villas",
        "trump-mansions",
        "rayana-mansions",
        "rayana-kingdom",
        "trump-executive-residences",
        "trump-park-residences",
        "lumaia",
        "marea",
        "tierra-viva",
        "the-astera",
        "dg1",
        "da-vinci",
        "w-residences",
        "urban-oasis",
        "the-mulliner",
        "les-vagues",
    ]

    if any(
        marker in url
        for marker in known_project_markers
    ):
        return True

    # --------------------------------------------------------
    # 5. Property-specific title language
    # --------------------------------------------------------

    property_title_markers = [
        "residences",
        "residence",
        "villa",
        "villas",
        "apartment",
        "apartments",
        "mansion",
        "mansions",
        "hotel residences",
        "townhouse",
        "townhouses",
        "penthouse",
        "penthouses",
    ]

    if any(
        marker in title
        for marker in property_title_markers
    ):
        return True

    return False


# ============================================================
# PRICE EXTRACTION
# ============================================================

def extract_price(text: str) -> Optional[str]:
    """
    Extract a monetary amount.

    This is only called for documents classified as
    property pages.

    Examples:

        AED 2 million
        AED 2M
        SAR 4M
        SAR 4 million
        OMR 500,000
        QAR 3,650,000
        USD 1.5 million
        £2 million
        $3M
    """

    patterns = [
        r"\bAED\s?[\d,]+(?:\.\d+)?(?:\s?(?:million|m|billion|bn))?\b",
        r"\bSAR\s?[\d,]+(?:\.\d+)?(?:\s?(?:million|m|billion|bn))?\b",
        r"\bOMR\s?[\d,]+(?:\.\d+)?(?:\s?(?:million|m|billion|bn))?\b",
        r"\bQAR\s?[\d,]+(?:\.\d+)?(?:\s?(?:million|m|billion|bn))?\b",
        r"\bUSD\s?[\d,]+(?:\.\d+)?(?:\s?(?:million|m|billion|bn))?\b",
        r"£[\d,]+(?:\.\d+)?(?:\s?(?:million|m|billion|bn))?",
        r"\$[\d,]+(?:\.\d+)?(?:\s?(?:million|m|billion|bn))?",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(0)

    return None


# ============================================================
# BEDROOM EXTRACTION
# ============================================================

def extract_bedrooms(
    text: str,
) -> Optional[int]:

    patterns = [
        r"\b(\d+)\s*[- ]?\s*bedrooms?\b",
        r"\b(\d+)\s*BR\b",
        r"\b(\d+)\s*bed\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            try:
                return int(
                    match.group(1)
                )

            except ValueError:
                pass

    return None


# ============================================================
# AREA EXTRACTION
# ============================================================

def extract_area(
    text: str,
) -> Optional[str]:

    patterns = [
        r"([\d,]+(?:\.\d+)?)\s*(?:sq\.?\s*ft|sqft|square feet)",
        r"([\d,]+(?:\.\d+)?)\s*m²",
        r"([\d,]+(?:\.\d+)?)\s*sqm",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(0)

    return None


# ============================================================
# DOCUMENT TYPE
# ============================================================

def detect_document_type(
    record: Dict[str, Any],
) -> str:

    url = str(
        record.get("source_url", "")
    ).lower()

    # --------------------------------------------------------
    # Press releases
    # --------------------------------------------------------

    if "/press/" in url:
        return "press_release"

    # --------------------------------------------------------
    # News
    # --------------------------------------------------------

    if "/news/" in url:
        return "news"

    # --------------------------------------------------------
    # Blog / insights
    # --------------------------------------------------------

    if (
        "/blog/" in url
        or "/insights/" in url
    ):
        return "article"

    # --------------------------------------------------------
    # Category/listing pages
    # --------------------------------------------------------

    if is_category_page(record):
        return "category"

    # --------------------------------------------------------
    # Individual property/project pages
    # --------------------------------------------------------

    if is_property_page(record):
        return "property"

    # --------------------------------------------------------
    # General pages
    # --------------------------------------------------------

    return "general"


# ============================================================
# MAIN NORMALIZATION
# ============================================================

def normalize_record(
    record: Dict[str, Any],
) -> Optional[Dict[str, Any]]:

    # --------------------------------------------------------
    # 1. Reject Cloudflare / bot challenge pages
    # --------------------------------------------------------

    if is_blocked_page(record):

        print(
            "Skipping blocked page: "
            f"{record.get('source_url', '')}"
        )

        return None

    # --------------------------------------------------------
    # 2. Basic fields
    # --------------------------------------------------------

    source = str(
        record.get("source", "")
    ).lower().strip()

    source_url = str(
        record.get("source_url", "")
    ).strip()

    title = clean_text(
        record.get("title")
    )

    description = clean_text(
        record.get("description")
    )

    content = clean_text(
        record.get("content")
    )

    combined_text = " ".join(
        value
        for value in [
            title,
            description,
            content,
        ]
        if value
    )

    if not combined_text:
        return None

    # --------------------------------------------------------
    # 3. Determine document type
    # --------------------------------------------------------

    document_type = detect_document_type(
        record
    )

    property_page = (
        document_type == "property"
    )

    # --------------------------------------------------------
    # 4. Property-specific fields
    # --------------------------------------------------------

    property_name = None
    developer = None
    brand = None
    country = None
    city = None
    location = None
    property_type = None
    investment = None
    investment_type = None

    price = None
    bedrooms = None
    area = None

    if property_page:

        property_name = extract_property_name(
            record
        )

        developer = extract_developer(
            record
        )

        brand = extract_brand(
            record
        )

        country = extract_country(
            record
        )

        city = extract_city(
            record
        )

        location = extract_location(
            record
        )

        property_type = extract_property_type(
            record
        )

        investment = extract_investment(
            record
        )

        investment_type = extract_investment_type(
            record
        )

        price = extract_price(
            combined_text
        )

        bedrooms = extract_bedrooms(
            combined_text
        )

        area = extract_area(
            combined_text
        )


    # --------------------------------------------------------
    # 5. Return normalized record
    # --------------------------------------------------------

    return {
        "source": source,
        "source_url": source_url,
        "title": title,
        "description": description,
        "content": content,

        "document_type": document_type,

        "property_name": property_name,
        "developer": developer,
        "brand": brand,
        "country": country,
        "city": city,
        "location": location,
        "property_type": property_type,

        "investment": investment,
        "investment_type": investment_type,

        "price": price,
        "bedrooms": bedrooms,
        "area": area,

        "scraped_at": record.get(
            "scraped_at"
        ),
    }
