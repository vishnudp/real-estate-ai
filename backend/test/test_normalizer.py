import pytest

from app.services.normalizer import (
    detect_document_type,
    is_blocked_page,
    is_category_page,
    is_property_page,
    normalize_record,
)


# ============================================================
# CATEGORY PAGE TESTS
# ============================================================


def test_properties_in_oman_is_category():
    record = {
        "source_url": (
            "https://darglobal.co.uk/"
            "projects/properties-in-oman"
        ),
        "title": "Properties in Oman",
        "description": "",
        "content": "",
    }

    assert is_category_page(record)
    assert not is_property_page(record)
    assert detect_document_type(record) == "category"


def test_properties_in_oman_apartments_is_category():
    record = {
        "source_url": (
            "https://darglobal.co.uk/"
            "projects/properties-in-oman/apartments"
        ),
        "title": "Apartments in Oman",
        "description": "",
        "content": "",
    }

    assert is_category_page(record)
    assert not is_property_page(record)
    assert detect_document_type(record) == "category"


def test_properties_in_uae_is_category():
    record = {
        "source_url": (
            "https://darglobal.co.uk/"
            "projects/properties-in-uae"
        ),
        "title": "Properties in UAE",
        "description": "",
        "content": "",
    }

    assert is_category_page(record)
    assert not is_property_page(record)
    assert detect_document_type(record) == "category"


# ============================================================
# PROPERTY PAGE TESTS
# ============================================================


def test_marriott_residences_oman_is_property():
    record = {
        "source_url": (
            "https://darglobal.co.uk/"
            "partners/marriott-residences-aida-oman"
        ),
        "title": (
            "Marriott Residences Oman | "
            "DarGlobal Branded Living"
        ),
        "description": (
            "Marriott Residences at AIDA, Muscat "
            "combine five-star hospitality with "
            "private ownership. A DarGlobal "
            "collaboration in Oman."
        ),
        "content": "",
    }

    assert is_property_page(record)
    assert not is_category_page(record)
    assert detect_document_type(record) == "property"


def test_trump_maldives_is_property():
    record = {
        "source_url": (
            "https://darglobal.co.uk/"
            "trump-international-resort-maldives"
        ),
        "title": (
            "Trump International Hotel & Resort Maldives"
        ),
        "description": (
            "Discover the first and only Trump "
            "International Hotel & Resort Maldives, "
            "a 5-star luxury retreat in Noonu Atoll "
            "featuring private lagoon villas, "
            "overwater residences, exclusive private "
            "islands, and unparalleled seclusion."
        ),
        "content": "",
    }

    assert is_property_page(record)
    assert not is_category_page(record)
    assert detect_document_type(record) == "property"


# ============================================================
# PROPERTY METADATA TESTS
# ============================================================


def test_marriott_residences_oman_metadata():
    record = {
        "source": "darglobal",
        "source_url": (
            "https://darglobal.co.uk/"
            "partners/marriott-residences-aida-oman"
        ),
        "title": (
            "Marriott Residences Oman | "
            "DarGlobal Branded Living"
        ),
        "description": (
            "Marriott Residences at AIDA, Muscat "
            "combine five-star hospitality with "
            "private ownership. A DarGlobal "
            "collaboration in Oman."
        ),
        "content": "",
    }

    normalized = normalize_record(record)

    assert normalized["document_type"] == "property"
    assert normalized["property_name"] == "Marriott Residences Oman"
    assert normalized["developer"] == "DarGlobal"
    assert normalized["brand"] == "Marriott"
    assert normalized["country"] == "Oman"
    assert normalized["city"] == "Muscat"
    assert normalized["location"] == "AIDA"
    assert normalized["property_type"] == "hotel_residences"
    assert normalized["investment_type"] == "private_ownership"


def test_trump_maldives_metadata():
    record = {
        "source": "darglobal",
        "source_url": (
            "https://darglobal.co.uk/"
            "trump-international-resort-maldives"
        ),
        "title": (
            "Trump International Hotel & Resort Maldives"
        ),
        "description": (
            "Discover the first and only Trump "
            "International Hotel & Resort Maldives, "
            "a 5-star luxury retreat in Noonu Atoll "
            "featuring private lagoon villas, "
            "overwater residences, exclusive private "
            "islands, and unparalleled seclusion."
        ),
        "content": (
            "Reasons to Invest in Maldives. "
            "Limited supply. Rental income and "
            "rental yield opportunities."
        ),
    }

    normalized = normalize_record(record)

    assert normalized["document_type"] == "property"
    assert normalized["property_name"] == (
        "Trump International Hotel & Resort Maldives"
    )
    assert normalized["developer"] == "DarGlobal"
    assert normalized["brand"] == "Trump"
    assert normalized["country"] == "Maldives"
    assert normalized["location"] == "Noonu Atoll"
    assert normalized["property_type"] == "hotel_resort"
    assert normalized["investment_type"] == "rental_income"
    assert normalized["investment"] is not None


# ============================================================
# CROSS-CONTAMINATION REGRESSION TEST
# ============================================================


def test_trump_maldives_does_not_inherit_marriott_or_oman_metadata():
    record = {
        "source": "darglobal",
        "source_url": (
            "https://darglobal.co.uk/"
            "trump-international-resort-maldives"
        ),
        "title": (
            "Trump International Hotel & Resort Maldives"
        ),
        "description": (
            "A luxury retreat in Noonu Atoll "
            "in the Maldives."
        ),
        "content": (
            "This page contains unrelated DarGlobal "
            "projects including Marriott Residences "
            "Oman, AIDA, Muscat and Doha."
        ),
    }

    normalized = normalize_record(record)

    assert normalized["document_type"] == "property"
    assert normalized["property_name"] == (
        "Trump International Hotel & Resort Maldives"
    )
    assert normalized["brand"] == "Trump"
    assert normalized["country"] == "Maldives"
    assert normalized["location"] == "Noonu Atoll"

    # These must not come from unrelated projects
    assert normalized["city"] is None
    assert normalized["location"] != "AIDA"


# ============================================================
# BLOCKED PAGE TEST
# ============================================================


def test_blocked_cloudflare_page_is_rejected():
    record = {
        "source": "wasalt",
        "source_url": "https://wasalt.com/",
        "title": "Just a moment...",
        "description": "",
        "content": (
            "Performing security verification. "
            "This website uses a security service "
            "to protect against malicious bots. "
            "Cloudflare."
        ),
    }

    assert is_blocked_page(record)

    normalized = normalize_record(record)

    # Blocked pages should not become usable documents.
    assert normalized is None
