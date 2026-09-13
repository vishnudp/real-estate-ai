import json
import hashlib
from pathlib import Path

from app.db.database import (
    Base,
    engine,
    SessionLocal,
)

from app.services.sqlite_store import (
    upsert_properties,
)

from app.services.normalizer import (
    is_property_record,
)

from app.knowledge.chroma_store import (
    add_documents,
    count,
    reset_collection,
)

from app.models.property import Property
from app.models.location import Location

from app.knowledge.chroma_store import (
    add_documents,
    count,
    reset_collection,
    check_record_ids,
)



ROOT = Path(__file__).resolve().parents[3]

INPUT_FILE = (
    ROOT
    / "data"
    / "normalized"
    / "properties.json"
)


def make_id(record: dict) -> str:
    """
    Generate a stable Chroma ID from the source URL.
    """

    source_url = record.get(
        "source_url",
        "",
    )

    return hashlib.md5(
        source_url.encode("utf-8")
    ).hexdigest()


def build_document(record: dict) -> str:
    """
    Convert a normalized record into text suitable
    for semantic retrieval.
    """

    parts = [
        f"Source: {record.get('source', '')}",
        f"Title: {record.get('title', '')}",
        f"Property: {record.get('property_name', '')}",
        f"Developer: {record.get('developer', '')}",
        f"Brand: {record.get('brand', '')}",
        f"Country: {record.get('country', '')}",
        f"City: {record.get('city', '')}",
        f"Location: {record.get('location', '')}",
        f"Property Type: {record.get('property_type', '')}",
        f"Investment Type: {record.get('investment_type', '')}",
        f"Description: {record.get('description', '')}",
        f"Content: {record.get('content', '')}",
    ]

    if record.get("price"):
        parts.append(
            f"Price: {record['price']}"
        )

    if record.get("bedrooms") is not None:
        parts.append(
            f"Bedrooms: {record['bedrooms']}"
        )

    if record.get("area"):
        parts.append(
            f"Area: {record['area']}"
        )

    parts.append(
        f"Source URL: {record.get('source_url', '')}"
    )

    return "\n".join(parts)


def build_metadata(
    record: dict,
    property_id: int | None = None,
) -> dict:
    """
    Build Chroma metadata.

    record_id:
        Stable ID for every Chroma record.

    property_id:
        SQLAlchemy Property.id.
        Only populated for actual property records.
    """

    brand = record.get("brand") or ""

    record_id = make_id(record)

    metadata = {
        # ---------------------------------------------
        # Every Chroma record gets this ID.
        # ---------------------------------------------
        "record_id": str(record_id),

        "source": str(
            record.get("source", "")
        ),

        "source_url": str(
            record.get("source_url", "")
        ),

        "title": str(
            record.get("title", "")
        ),

        "property_name": str(
            record.get("property_name")
            or ""
        ),

        "developer": str(
            record.get("developer")
            or ""
        ),

        "brand": str(
            brand
        ),

        "country": str(
            record.get("country")
            or ""
        ),

        "city": str(
            record.get("city")
            or ""
        ),

        "location": str(
            record.get("location")
            or ""
        ),

        "property_type": str(
            record.get("property_type")
            or ""
        ),

        "investment_type": str(
            record.get("investment_type")
            or ""
        ),

        "document_type": str(
            record.get(
                "document_type",
                "general",
            )
        ),

        "price": str(
            record.get("price")
            or ""
        ),

        "bedrooms": str(
            record.get("bedrooms")
            if record.get("bedrooms") is not None
            else ""
        ),

        "area": str(
            record.get("area")
            or ""
        ),

        "scraped_at": str(
            record.get("scraped_at")
            or ""
        ),
    }

    # ---------------------------------------------
    # Only actual properties get SQL property_id.
    # ---------------------------------------------
    if property_id is not None:
        metadata["property_id"] = str(
            property_id
        )

    return metadata

def main():

    if not INPUT_FILE.exists():

        print(
            f"Input file not found: {INPUT_FILE}"
        )

        return

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        records = json.load(f)

    print(
        f"Loaded {len(records)} normalized records"
    )

    # --------------------------------------------------------
    # FILTER INDIVIDUAL PROPERTY RECORDS
    # --------------------------------------------------------

    property_records = []

    for record in records:

        if is_property_record(record):

            property_records.append(record)

        else:

            print(
                "Skipping non-property record:",
                record.get("source_url"),
            )

    print(
        f"Actual property records: "
        f"{len(property_records)}"
    )

    # --------------------------------------------------------
    # SQLITE
    # --------------------------------------------------------

    Base.metadata.create_all(
        bind=engine
    )

    db = SessionLocal()

    try:

        sqlite_count = upsert_properties(
            db=db,
            records=property_records,
        )

        print(
            f"SQLite properties upserted: "
            f"{sqlite_count}"
        )

        # ----------------------------------------------------
        # BUILD source_url -> Property.id MAPPING
        # ----------------------------------------------------

        property_id_by_url = {}

        properties = (
            db.query(Property)
            .filter(
                Property.source_url.isnot(None)
            )
            .all()
        )

        for property_item in properties:

            if property_item.source_url:

                property_id_by_url[
                    property_item.source_url
                ] = property_item.id

        print(
            f"Database property IDs found: "
            f"{len(property_id_by_url)}"
        )

    finally:

        db.close()

    # --------------------------------------------------------
    # CHROMADB
    #
    # Keep ALL normalized records here.
    #
    # Property pages, category pages and press/news pages
    # are all useful as semantic knowledge.
    # --------------------------------------------------------

    reset_collection()

    documents = []
    metadatas = []
    ids = []

    property_metadata_count = 0

    for record in records:

        source_url = record.get(
            "source_url"
        )

        if not source_url:
            continue

        property_id = (
            property_id_by_url.get(
                source_url
            )
        )

        if property_id is not None:
            property_metadata_count += 1

        documents.append(
            build_document(record)
        )

        metadatas.append(
            build_metadata(
                record,
                property_id=property_id,
            )
        )

        ids.append(
            make_id(record)
        )

    add_documents(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )

    print(
        f"ChromaDB indexed: "
        f"{len(documents)}"
    )

    print(
        f"ChromaDB records linked to "
        f"Property IDs: "
        f"{property_metadata_count}"
    )

    print(
        f"ChromaDB total documents: "
        f"{count()}"
    )


if __name__ == "__main__":
    main()

print(
    f"ChromaDB total documents: "
    f"{count()}"
)

check_record_ids()
