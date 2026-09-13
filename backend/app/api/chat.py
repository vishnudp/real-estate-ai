from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.property import Property

from app.schemas.property import (
    ChatRequest,
    ChatResponse,
)

from app.services.query_understanding import (
    understand_query,
)

from app.services.hybrid_search import (
    hybrid_search,
)

from app.services.property_analysis import (
    analyze_property,
)

from app.services.investment_engine import (
    InvestmentEngine,
)


router = APIRouter(
    prefix="/api/chat",
    tags=["chat"],
)


investment_engine = InvestmentEngine()


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def resolve_semantic_property(
    db: Session,
    semantic_item: dict,
) -> Property | None:
    """
    Resolve a semantic-search result back to a database Property.

    Semantic search results may not contain the SQL property ID.
    We therefore try stable identifiers in this order:

    1. source_url
    2. project_name / property_name
    3. title
    """

    metadata = semantic_item.get(
        "metadata",
        {},
    )

    source_url = metadata.get(
        "source_url"
    )

    property_name = (
        metadata.get("property_name")
        or metadata.get("project_name")
        or metadata.get("title")
    )

    # --------------------------------------------------------------
    # Match by source URL
    # --------------------------------------------------------------

    if source_url:
        property_item = (
            db.query(Property)
            .filter(
                Property.source_url == source_url
            )
            .first()
        )

        if property_item:
            return property_item

    # --------------------------------------------------------------
    # Match by project name
    # --------------------------------------------------------------

    if property_name:
        property_item = (
            db.query(Property)
            .filter(
                Property.project_name == property_name
            )
            .first()
        )

        if property_item:
            return property_item

    # --------------------------------------------------------------
    # Match by title
    # --------------------------------------------------------------

    if property_name:
        property_item = (
            db.query(Property)
            .filter(
                Property.title == property_name
            )
            .first()
        )

        if property_item:
            return property_item

    return None


def property_to_dict(
    property_item: Property,
) -> dict:
    """
    Convert a SQL Property model into the dictionary structure
    already used by the chat/search response.
    """

    return {
        "id": property_item.id,
        "title": property_item.title,
        "project_name": property_item.project_name,
        "developer": property_item.developer,
        "property_type": property_item.property_type,
        "country": property_item.country,
        "city": property_item.city,
        "location": property_item.location,
        "price": property_item.price,
        "currency": property_item.currency,
        "bedrooms": property_item.bedrooms,
        "bathrooms": property_item.bathrooms,
        "area": property_item.area,
        "area_unit": property_item.area_unit,
        "listing_type": property_item.listing_type,
        "status": property_item.status,
        "brands": property_item.brands,
        "source": property_item.source,
        "source_url": property_item.source_url,
    }


def resolve_properties(
    db: Session,
    structured_results: list[dict],
    semantic_results: list[dict],
) -> list[dict]:
    """
    Build a unified list of database-backed properties.

    Structured results already contain database IDs.

    Semantic results may only contain Chroma metadata, so those
    are resolved back to the SQL Property table.
    """

    resolved = []
    seen_ids = set()

    # --------------------------------------------------------------
    # Structured results
    # --------------------------------------------------------------

    for property_item in structured_results:

        property_id = property_item.get("id")

        if property_id is None:
            continue

        if property_id in seen_ids:
            continue

        resolved.append(
            property_item
        )

        seen_ids.add(
            property_id
        )

    # --------------------------------------------------------------
    # Semantic results
    # --------------------------------------------------------------

    for semantic_item in semantic_results:

        property_item = resolve_semantic_property(
            db,
            semantic_item,
        )

        if property_item is None:
            continue

        property_id = property_item.id

        if property_id in seen_ids:
            continue

        resolved.append(
            property_to_dict(
                property_item
            )
        )

        seen_ids.add(
            property_id
        )

    return resolved


def build_property_analysis(
    db: Session,
    properties: list[dict],
) -> list[dict]:
    """
    Run the complete property intelligence pipeline.

    analyze_property() is intentionally the single source of truth
    for:

    - property information
    - location
    - infrastructure
    - comparables
    - intelligence
    - valuation
    - confidence
    """

    analysis = []

    for property_item in properties:

        property_id = property_item.get(
            "id"
        )

        if property_id is None:
            continue

        property_analysis = analyze_property(
            db,
            property_id,
        )

        analysis.append(
            {
                "property_id": property_id,
                "analysis": property_analysis,
            }
        )

    return analysis


def build_investment_analysis(
    analysis: list[dict],
) -> list[dict]:
    """
    Return the investment analysis already calculated by
    analyze_property().

    analyze_property() is the single source of truth for
    investment analysis.
    """

    investment = []

    for item in analysis:

        property_id = item.get(
            "property_id"
        )

        if property_id is None:
            continue

        property_analysis = item.get(
            "analysis",
            {},
        )

        investment_result = property_analysis.get(
            "investment",
            {},
        )

        investment.append(
            {
                "property_id": property_id,
                "investment": investment_result,
            }
        )

    return investment



# ------------------------------------------------------------------
# Message builders
# ------------------------------------------------------------------


def build_message(
    query: str,
    understood: dict,
    results: list[dict],
    semantic_results: list[dict],
    analysis: list[dict] | None = None,
    investment: list[dict] | None = None,
) -> str:
    """
    Build a concise natural-language response.

    The API still returns the complete structured intelligence
    separately in `analysis` and `investment`.
    """

    analysis = analysis or []
    investment = investment or []

    intent = understood.get(
        "intent"
    )

    # --------------------------------------------------------------
    # Investment analysis
    # --------------------------------------------------------------

    if intent == "investment_analysis":

        if not analysis:

            if semantic_results:
                return (
                    "I found relevant information for your query, "
                    "but I could not resolve the property to a "
                    "database record for investment analysis."
                )

            return (
                "I couldn't find a property record that I can "
                "reliably assess for investment."
            )

        item = analysis[0]

        property_analysis = item.get(
            "analysis",
            {},
        )

        property_data = property_analysis.get(
            "property",
            {},
        )

        project_name = (
            property_data.get(
                "project_name"
            )
            or property_data.get(
                "title"
            )
            or "This property"
        )

        result = None

        if investment:
            result = investment[0].get(
                "investment",
                {}
            )

        if not result:
            return (
                f"I analyzed {project_name}, but there is "
                "not enough information to produce an investment "
                "assessment."
            )

        decision = result.get(
            "decision"
        )

        summary = result.get(
            "summary"
        )

        if summary:
            message = summary
        else:
            message = (
                f"{project_name} has been assessed using the "
                "available property, infrastructure, comparable "
                "and valuation evidence."
            )

        # ----------------------------------------------------------
        # Infrastructure
        # ----------------------------------------------------------

        metrics = result.get(
            "metrics",
            {}
        )

        infrastructure_score = metrics.get(
            "infrastructure_score"
        )

        if infrastructure_score is not None:
            message += (
                f" Infrastructure score: "
                f"{infrastructure_score}/100."
            )

        # ----------------------------------------------------------
        # Valuation
        # ----------------------------------------------------------

        valuation = result.get(
            "valuation",
            {}
        )

        valuation_available = valuation.get(
            "available",
            False,
        )

        estimated_value = valuation.get(
            "estimated_value"
        )

        upside = valuation.get(
            "upside_percent"
        )

        currency = (
            property_data.get(
                "currency"
            )
            or ""
        )

        if valuation_available:

            if estimated_value is not None:
                message += (
                    f" Estimated fair value: "
                    f"{currency} "
                    f"{estimated_value:,.0f}."
                )

            if upside is not None:
                message += (
                    f" Estimated upside versus asking "
                    f"price: {upside:.1f}%."
                )

        else:

            target_area = property_data.get(
                "area"
            )

            target_price = property_data.get(
                "price"
            )

            if target_price is None and target_area is None:
                message += (
                    " A reliable property valuation cannot "
                    "yet be calculated because the unit price "
                    "and property area are not available."
                )

            elif target_price is None:
                message += (
                    " A reliable property valuation cannot "
                    "yet be calculated because the unit "
                    "asking price is not available."
                )

            elif target_area is None:
                message += (
                    " A reliable property valuation cannot "
                    "yet be calculated because the property "
                    "area is not available."
                )


        # ----------------------------------------------------------
        # Investment decision
        # ----------------------------------------------------------

        recommendation = result.get(
            "recommendation"
        )

        if recommendation:
            message += (
                f" Investment assessment: "
                f"{recommendation.replace('_', ' ')}."
            )
        elif decision:
            message += (
                f" Investment assessment: "
                f"{decision.replace('_', ' ')}."
            )

        return message

    # --------------------------------------------------------------
    # Valuation
    # --------------------------------------------------------------

    if intent == "valuation":

        if not analysis:

            if semantic_results:
                return (
                    "I found the property information, but I "
                    "could not resolve it to a database property "
                    "record for valuation."
                )

            return (
                "I couldn't find enough property information "
                "to calculate a valuation."
            )

        property_analysis = analysis[0].get(
            "analysis",
            {}
        )

        property_data = property_analysis.get(
            "property",
            {}
        )

        project_name = (
            property_data.get(
                "project_name"
            )
            or property_data.get(
                "title"
            )
            or "This property"
        )

        valuation = property_analysis.get(
            "valuation",
            {}
        )

        if not valuation.get(
            "available",
            False,
        ):

            reason = valuation.get(
                "reason"
            ) or "There is insufficient data."

            return (
                f"I couldn't calculate a reliable valuation "
                f"for {project_name}. {reason}."
            )

        currency = (
            property_data.get(
                "currency"
            )
            or ""
        )

        estimated_value = valuation.get(
            "estimated_value"
        )

        fair_low = valuation.get(
            "fair_value_low"
        )

        fair_high = valuation.get(
            "fair_value_high"
        )

        message = (
            f"The estimated fair value of {project_name} "
            f"is {currency} {estimated_value:,.0f}."
        )

        if fair_low is not None and fair_high is not None:
            message += (
                f" The estimated fair-value range is "
                f"{currency} {fair_low:,.0f} to "
                f"{currency} {fair_high:,.0f}."
            )

        upside = valuation.get(
            "upside_percent"
        )

        if upside is not None:
            message += (
                f" This represents an estimated "
                f"{upside:.1f}% "
                f"{'upside' if upside >= 0 else 'downside'} "
                "versus the asking price."
            )

        return message

    # --------------------------------------------------------------
    # No retrieval
    # --------------------------------------------------------------

    if not results and not semantic_results:
        return (
            "I couldn't find any information matching "
            f'your query: "{query}".'
        )

    # --------------------------------------------------------------
    # Semantic-only result
    # --------------------------------------------------------------

    if not results and semantic_results:

        if analysis:
            property_analysis = analysis[0].get(
                "analysis",
                {}
            )

            property_data = property_analysis.get(
                "property",
                {}
            )

            name = (
                property_data.get(
                    "project_name"
                )
                or property_data.get(
                    "title"
                )
                or "the property"
            )

            return (
                f"I found {name} and analyzed the available "
                "property intelligence."
            )

        return (
            "I found relevant information for your query."
        )

    # --------------------------------------------------------------
    # Single property
    # --------------------------------------------------------------

    if len(results) == 1:

        property_item = results[0]

        name = (
            property_item.get(
                "project_name"
            )
            or property_item.get(
                "title"
            )
            or "This property"
        )

        location_parts = [
            property_item.get(
                "location"
            ),
            property_item.get(
                "city"
            ),
            property_item.get(
                "country"
            ),
        ]

        location = ", ".join(
            str(part)
            for part in location_parts
            if part
        )

        developer = property_item.get(
            "developer"
        )

        brands = property_item.get(
            "brands"
        )

        brand = None

        if brands:
            if isinstance(
                brands,
                list,
            ):
                brand = ", ".join(
                    str(item)
                    for item in brands
                )
            else:
                brand = str(
                    brands
                )

        message = (
            f"{name} is available"
        )

        if location:
            message += (
                f" at {location}"
            )

        if developer:
            message += (
                f" and is developed by "
                f"{developer}"
            )

        if brand:
            message += (
                f" with {brand} branding"
            )

        message += "."

        # ----------------------------------------------------------
        # Intelligence
        # ----------------------------------------------------------

        if analysis:

            property_analysis = analysis[0].get(
                "analysis",
                {}
            )

            infrastructure = property_analysis.get(
                "infrastructure",
                {}
            )

            infrastructure_score = infrastructure.get(
                "infrastructure_score"
            )

            if infrastructure_score is None:
                infrastructure_score = infrastructure.get(
                    "score"
                )

            if infrastructure_score is not None:
                message += (
                    f" Infrastructure score: "
                    f"{infrastructure_score}/100."
                )

            categories = infrastructure.get(
                "categories",
                {}
            )

            infrastructure_highlights = []

            for category, data in categories.items():

                if not isinstance(
                    data,
                    dict,
                ):
                    continue

                nearest = data.get(
                    "nearest"
                )

                if not nearest:
                    continue

                nearest_name = nearest.get(
                    "name"
                )

                distance = nearest.get(
                    "distance_km"
                )

                if (
                    nearest_name
                    and distance is not None
                ):
                    infrastructure_highlights.append(
                        f"{nearest_name} is "
                        f"{distance} km away"
                    )

            if infrastructure_highlights:
                message += (
                    " Nearby infrastructure includes "
                    + ", ".join(
                        infrastructure_highlights[:3]
                    )
                    + "."
                )

            # ------------------------------------------------------
            # Comparable market analysis
            # ------------------------------------------------------

            comparables = property_analysis.get(
                "comparables",
                {}
            )

            comparable_metrics = comparables.get(
                "metrics",
                {}
            )

            comparable_count = comparable_metrics.get(
                "priced_comparables",
                0
            )

            average_price = comparable_metrics.get(
                "average_price"
            )

            median_price = comparable_metrics.get(
                "median_price"
            )

            average_price_per_area = comparable_metrics.get(
                "average_price_per_area"
            )

            currency = (
                property_item.get(
                    "currency"
                )
                or ""
            )

            if comparable_count:

                message += (
                    f" I found {comparable_count} priced "
                    "comparable properties."
                )

                if average_price is not None:
                    message += (
                        f" Their average price is "
                        f"{currency} "
                        f"{average_price:,.0f}"
                    )

                if median_price is not None:
                    message += (
                        f", with a median of "
                        f"{currency} "
                        f"{median_price:,.0f}"
                    )

                if average_price_per_area is not None:
                    message += (
                        f" and an average price per "
                        f"sqm of "
                        f"{currency} "
                        f"{average_price_per_area:,.2f}"
                    )

                message += "."

        return message

    # --------------------------------------------------------------
    # Multiple properties
    # --------------------------------------------------------------

    return (
        f"I found {len(results)} properties "
        "matching your query."
    )


# ------------------------------------------------------------------
# API endpoint
# ------------------------------------------------------------------


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    query = request.message.strip()

    understood = understand_query(
        query
    )

    # --------------------------------------------------------------
    # Retrieval
    # --------------------------------------------------------------

    retrieval = hybrid_search(
        db=db,
        query=query,
        filters=understood,
        brand=understood.get(
            "brand"
        ),
        country=understood.get(
            "country"
        ),
        city=understood.get(
            "city"
        ),
        property_type=understood.get(
            "property_type"
        ),
    )

    structured_results = retrieval.get(
        "results",
        []
    )

    semantic_results = retrieval.get(
        "semantic_results",
        []
    )

    # --------------------------------------------------------------
    # Resolve all properties.
    #
    # This is important for investment/valuation queries because
    # semantic search may find the property while structured search
    # intentionally returns no rows.
    # --------------------------------------------------------------

    resolved_properties = resolve_properties(
        db=db,
        structured_results=structured_results,
        semantic_results=semantic_results,
    )

    # --------------------------------------------------------------
    # Property intelligence
    # --------------------------------------------------------------

    analysis = build_property_analysis(
        db=db,
        properties=resolved_properties,
    )

    # --------------------------------------------------------------
    # Investment analysis
    # --------------------------------------------------------------

    investment = []

    if understood.get(
        "intent"
    ) == "investment_analysis":

        investment = build_investment_analysis(
            analysis
        )

    # --------------------------------------------------------------
    # Build response message
    # --------------------------------------------------------------

    message = build_message(
        query=query,
        understood=understood,
        results=structured_results,
        semantic_results=semantic_results,
        analysis=analysis,
        investment=investment,
    )

    # --------------------------------------------------------------
    # API response
    # --------------------------------------------------------------

    return {
        "message": message,
        "intent": understood.get(
            "intent",
            "general",
        ),
        "filters": {
            key: value
            for key, value in understood.items()
            if key != "query"
            and value is not None
        },
        "results": structured_results,
        "semantic_results": semantic_results,
        "analysis": analysis,
        "investment": investment,
    }
