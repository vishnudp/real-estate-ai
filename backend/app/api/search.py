from fastapi import APIRouter, Query

from app.knowledge.chroma_store import (
    search,
    get_by_record_id,
)


router = APIRouter(
    prefix="/api/search",
    tags=["search"],
)


def _format_match(
    document: str,
    metadata: dict,
    chroma_id: str | None = None,
) -> dict:
    """
    Convert a Chroma record into the API response format.

    Important:
    - property_id = SQL database Property ID when available
    - record_id = Chroma record identifier
    - chroma_id = actual Chroma document ID
    """

    property_id = metadata.get("property_id")
    record_id = metadata.get("record_id")

    return {
        "id": (
            int(property_id)
            if property_id
            else None
        ),

        "property_id": (
            int(property_id)
            if property_id
            else None
        ),

        "record_id": record_id,

        "chroma_id": chroma_id,

        "document": document,

        "metadata": metadata,
    }


@router.get("")
def semantic_search(
    q: str = Query(
        ...,
        min_length=1,
    ),
    limit: int = Query(
        default=5,
        ge=1,
        le=20,
    ),
    property_only: bool = Query(
        default=False,
        description="Return only actual property records",
    ),
):
    """
    Search properties.

    Search order:

    1. Exact Chroma record_id lookup.
    2. Semantic Chroma search.

    This allows queries such as:

        a1bc550a382c964081ee7aca4511f9f7

    to find the exact Chroma record instead of performing
    semantic search.
    """

    query = q.strip()

    if not query:
        return {
            "query": q,
            "property_only": property_only,
            "results": [],
        }

    # =========================================================
    # 1. EXACT RECORD ID SEARCH
    # =========================================================

    exact_record = get_by_record_id(query)

    if exact_record:

        metadata = (
            exact_record.get("metadata")
            or {}
        )

        # Respect property_only.
        if (
            property_only
            and metadata.get("document_type")
            != "property"
        ):
            return {
                "query": q,
                "property_only": property_only,
                "results": [],
            }

        return {
            "query": q,
            "property_only": property_only,
            "results": [
                _format_match(
                    document=exact_record.get(
                        "document",
                        "",
                    ),
                    metadata=metadata,
                    chroma_id=exact_record.get(
                        "id"
                    ),
                )
            ],
        }

    # =========================================================
    # 2. SEMANTIC SEARCH
    # =========================================================

    filters = None

    if property_only:
        filters = {
            "document_type": "property",
        }

    results = search(
        query=query,
        n_results=limit,
        filters=filters,
    )

    documents = (
        results.get(
            "documents",
            [[]],
        )[0]
    )

    metadatas = (
        results.get(
            "metadatas",
            [[]],
        )[0]
    )

    chroma_ids = (
        results.get(
            "ids",
            [[]],
        )[0]
    )

    matches = []

    for index, document in enumerate(
        documents
    ):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )

        chroma_id = (
            chroma_ids[index]
            if index < len(chroma_ids)
            else None
        )

        matches.append(
            _format_match(
                document=document,
                metadata=metadata,
                chroma_id=chroma_id,
            )
        )

    return {
        "query": q,
        "property_only": property_only,
        "results": matches,
    }
