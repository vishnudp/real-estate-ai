import os

from pathlib import Path
from typing import List, Dict, Any

import chromadb

from chromadb.utils.embedding_functions import (
    DefaultEmbeddingFunction,
)



ROOT = Path(__file__).resolve().parents[3]

# CHROMA_PATH = ROOT / "data" / "chroma"

CHROMA_PATH = Path(
    os.getenv(
        "CHROMA_PATH",
        "./data/chroma",
    )
)


CHROMA_PATH.mkdir(
    parents=True,
    exist_ok=True,
)

embedding_function = DefaultEmbeddingFunction()


client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


COLLECTION_NAME = "real_estate_knowledge"

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={
        "description": (
            "DarGlobal and Wasalt real estate knowledge"
        )
    },
    embedding_function=embedding_function,
)


# =========================================================
# ADD / UPSERT
# =========================================================

def add_documents(
    documents: List[str],
    metadatas: List[Dict[str, Any]],
    ids: List[str],
):
    """
    Add or update documents in ChromaDB.

    Every Chroma record must have a unique ID.
    """

    if not documents:
        return

    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )


# =========================================================
# SEMANTIC SEARCH
# =========================================================

def search(
    query: str,
    n_results: int = 5,
    distance_threshold: float = 1.2,
    filters: Dict[str, Any] | None = None,
):
    """
    Semantic search against the real estate knowledge base.

    Optional metadata filters:
    - country
    - city
    - brand
    - property_type
    - document_type
    """

    if not query or not query.strip():
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
            "ids": [[]],
        }

    where = None

    if filters:
        conditions = []

        for key, value in filters.items():

            if value is None:
                continue

            value = str(value).strip()

            if not value:
                continue

            conditions.append(
                {
                    key: value,
                }
            )

        if len(conditions) == 1:
            where = conditions[0]

        elif len(conditions) > 1:
            where = {
                "$and": conditions,
            }

    query_kwargs = {
        "query_texts": [query],
        "n_results": n_results,
        "include": [
            "documents",
            "metadatas",
            "distances",
        ],
    }

    if where:
        query_kwargs["where"] = where

    try:
        results = collection.query(
            **query_kwargs
        )

    except Exception as exc:

        print(
            f"Chroma semantic search failed: {exc}"
        )

        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
            "ids": [[]],
        }

    documents = (
        results.get("documents") or [[]]
    )[0]

    metadatas = (
        results.get("metadatas") or [[]]
    )[0]

    distances = (
        results.get("distances") or [[]]
    )[0]

    chroma_ids = (
        results.get("ids") or [[]]
    )[0]

    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []
    filtered_ids = []

    for index, distance in enumerate(distances):

        if distance > distance_threshold:
            continue

        filtered_documents.append(
            documents[index]
        )

        filtered_metadatas.append(
            metadatas[index]
        )

        filtered_distances.append(
            distance
        )

        if index < len(chroma_ids):
            filtered_ids.append(
                chroma_ids[index]
            )
        else:
            filtered_ids.append(None)

    return {
        "documents": [
            filtered_documents
        ],
        "metadatas": [
            filtered_metadatas
        ],
        "distances": [
            filtered_distances
        ],
        "ids": [
            filtered_ids
        ],
    }


# =========================================================
# RECORD ID SEARCH
# =========================================================

def get_by_record_id(
    record_id: str,
) -> dict | None:
    """
    Find one Chroma record using its record_id.

    Example:

        a1bc550a382c964081ee7aca4511f9f7
    """

    if not record_id:
        return None

    record_id = str(record_id).strip()

    if not record_id:
        return None

    try:
        results = collection.get(
            where={
                "record_id": record_id,
            },
            include=[
                "documents",
                "metadatas",
            ],
        )

    except Exception as exc:

        print(
            f"Chroma record lookup failed: {exc}"
        )

        return None

    ids = results.get("ids") or []
    documents = results.get("documents") or []
    metadatas = results.get("metadatas") or []

    if not ids:
        return None

    return {
        "id": ids[0],

        "record_id": (
            metadatas[0].get("record_id")
            if metadatas
            else record_id
        ),

        "property_id": (
            metadatas[0].get("property_id")
            if metadatas
            else None
        ),

        "document": (
            documents[0]
            if documents
            else ""
        ),

        "metadata": (
            metadatas[0]
            if metadatas
            else {}
        ),
    }


# =========================================================
# DIRECT CHROMA ID LOOKUP
# =========================================================

def get_by_chroma_id(
    chroma_id: str,
) -> dict | None:
    """
    Find a record directly using the Chroma document ID.

    In your current ingestion process the Chroma ID and
    record_id are normally the same value.
    """

    if not chroma_id:
        return None

    chroma_id = str(chroma_id).strip()

    if not chroma_id:
        return None

    try:
        results = collection.get(
            ids=[chroma_id],
            include=[
                "documents",
                "metadatas",
            ],
        )

    except Exception as exc:

        print(
            f"Chroma ID lookup failed: {exc}"
        )

        return None

    ids = results.get("ids") or []
    documents = results.get("documents") or []
    metadatas = results.get("metadatas") or []

    if not ids:
        return None

    metadata = (
        metadatas[0]
        if metadatas
        else {}
    )

    return {
        "id": ids[0],
        "record_id": metadata.get(
            "record_id"
        ),
        "property_id": metadata.get(
            "property_id"
        ),
        "document": (
            documents[0]
            if documents
            else ""
        ),
        "metadata": metadata,
    }


# =========================================================
# COUNT
# =========================================================

def count() -> int:
    return collection.count()


# =========================================================
# RESET
# =========================================================

def reset_collection():
    """
    Delete and recreate the ChromaDB collection.

    Used when rebuilding the knowledge index.
    """

    global collection

    try:
        client.delete_collection(
            name=COLLECTION_NAME
        )

    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": (
                "DarGlobal and Wasalt real estate knowledge"
            )
        },
    )


# =========================================================
# VERIFY RECORD IDS
# =========================================================

def verify_record_ids():
    """
    Verify that every Chroma document has a record_id.
    """

    data = collection.get(
        include=["metadatas"]
    )

    metadatas = data.get(
        "metadatas",
        []
    )

    total = len(metadatas)

    with_record_id = 0
    without_record_id = 0

    missing = []

    for index, metadata in enumerate(metadatas):

        record_id = (
            metadata.get("record_id")
            if metadata
            else None
        )

        if record_id:
            with_record_id += 1

        else:
            without_record_id += 1

            missing.append(index)

    print(
        f"Total Chroma records: {total}"
    )

    print(
        f"Records with record_id: "
        f"{with_record_id}"
    )

    print(
        f"Records WITHOUT record_id: "
        f"{without_record_id}"
    )

    if missing:

        print(
            "Missing record_id indexes:",
            missing,
        )

    return {
        "total": total,
        "with_record_id": with_record_id,
        "without_record_id": without_record_id,
        "missing": missing,
    }


# =========================================================
# CHECK RECORD IDS
# =========================================================

def check_record_ids():

    data = collection.get(
        include=["metadatas"]
    )

    ids = data.get("ids", [])
    metadatas = data.get("metadatas", [])

    print(
        f"Total Chroma records: {len(ids)}"
    )

    missing_record_ids = []
    missing_property_ids = []

    for index, chroma_id in enumerate(ids):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )

        record_id = metadata.get(
            "record_id"
        )

        property_id = metadata.get(
            "property_id"
        )

        if not record_id:

            missing_record_ids.append(
                {
                    "chroma_id": chroma_id,
                    "source_url": metadata.get(
                        "source_url"
                    ),
                }
            )

        if not property_id:

            missing_property_ids.append(
                {
                    "chroma_id": chroma_id,
                    "record_id": record_id,
                    "source_url": metadata.get(
                        "source_url"
                    ),
                }
            )

    print(
        f"Records with record_id: "
        f"{len(ids) - len(missing_record_ids)}"
    )

    print(
        f"Records missing record_id: "
        f"{len(missing_record_ids)}"
    )

    print(
        f"Records with property_id: "
        f"{len(ids) - len(missing_property_ids)}"
    )

    print(
        f"Records missing property_id: "
        f"{len(missing_property_ids)}"
    )

    if missing_record_ids:

        print(
            "\nMissing record_id:"
        )

        for item in missing_record_ids:
            print(item)

    if missing_property_ids:

        print(
            "\nMissing property_id:"
        )

        for item in missing_property_ids:
            print(item)

    return {
        "total": len(ids),
        "missing_record_ids": missing_record_ids,
        "missing_property_ids": missing_property_ids,
    }
