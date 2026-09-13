from typing import Any

from sqlalchemy.orm import Session

from app.models.property import Property

from app.services.comparable_engine import (
calculate_comparable_metrics,
find_comparables,
)

from app.services.infrastructure_engine import (
analyze_property_infrastructure,
)

from app.ai.analysis_builder import (
build_property_intelligence,
)

from app.services.valuation_engine import (
valuation_engine,
)

from app.services.growth_engine import (
growth_engine,
)

from app.services.risk_engine import (
risk_engine,
)

from app.services.personalization_engine import (
    PersonalizationEngine,
)

from app.services.investment_engine import (investment_engine)

from app.services.deal_engine import deal_engine


def analyze_property(
db: Session,
property_id: int,
investor_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Generate a combined intelligence report for a property.

    Combines:

    - property information
    - location information
    - infrastructure analysis
    - comparable properties
    - comparable market metrics
    - valuation
    - growth analysis
    - risk analysis

    Important:
    Growth and risk are calculated explicitly here and then injected
    back into the intelligence object so downstream investment analysis
    uses the actual calculated values.
    """

    # ---------------------------------------------------------
    # Property
    # ---------------------------------------------------------
    personalization_engine = PersonalizationEngine()

    property_item = (
        db.query(Property)
        .filter(Property.id == property_id)
        .first()
    )

    if not property_item:
        return {
            "property_found": False,
            "property_id": property_id,
        }

    # ---------------------------------------------------------
    # Location
    # ---------------------------------------------------------

    location = None

    if property_item.location_record:
        location = {
            "id": property_item.location_record.id,
            "name": property_item.location_record.name,
            "type": property_item.location_record.location_type,
            "city": property_item.location_record.city,
            "country": property_item.location_record.country,
            "area": property_item.location_record.area,
            "address": property_item.location_record.address,
            "latitude": property_item.location_record.latitude,
            "longitude": property_item.location_record.longitude,
        }

    # ---------------------------------------------------------
    # Infrastructure
    # ---------------------------------------------------------

    infrastructure = analyze_property_infrastructure(
        db,
        property_id,
    )

    # ---------------------------------------------------------
    # Comparable properties
    # ---------------------------------------------------------

    comparable_result = find_comparables(
        db,
        property_id=property_id,
        limit=10,
    )

    comparable_items = comparable_result.get(
        "comparables",
        [],
    )

    comparable_count = comparable_result.get(
        "comparable_count",
        0,
    )

    comparable_metrics = calculate_comparable_metrics(
        comparable_result,
    )

    # ---------------------------------------------------------
    # Target property
    # ---------------------------------------------------------

    target = {
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
    }

    # ---------------------------------------------------------
    # Property intelligence
    # ---------------------------------------------------------

    intelligence = build_property_intelligence(
        property_data={
            **target,
            "description": property_item.description,
            "brands": property_item.brands,
        },
        infrastructure_data=infrastructure,
        comparable_data=comparable_result,
        comparable_metrics=comparable_metrics,
    )

    # Ensure intelligence is always a dictionary.
    if not isinstance(intelligence, dict):
        intelligence = {}

    # ---------------------------------------------------------
    # Valuation
    # ---------------------------------------------------------

    valuation = valuation_engine.calculate_valuation(
        target=target,
        comparables=comparable_items,
    )

    if not isinstance(valuation, dict):
        valuation = {}

    # ---------------------------------------------------------
    # Growth
    # ---------------------------------------------------------

    growth = growth_engine.calculate_growth(
        property_data=target,
        infrastructure=infrastructure,
        comparables={
            "items": comparable_items,
            "count": comparable_count,
            "metrics": comparable_metrics,
        },
        valuation=valuation,
        intelligence=intelligence,
    )

    if not isinstance(growth, dict):
        growth = {}

    # ---------------------------------------------------------
    # CRITICAL FIX
    #
    # Inject the freshly calculated growth result into intelligence.
    #
    # Previously build_property_intelligence() could contain an older
    # or empty growth object. InvestmentEngine reads:
    #
    #     intelligence["growth"]
    #
    # so it must receive the calculated growth result.
    # ---------------------------------------------------------

    intelligence["growth"] = growth

    # ---------------------------------------------------------
    # Risk
    # ---------------------------------------------------------

    risk = risk_engine.assess(
        property_data=target,
        intelligence=intelligence,
        valuation=valuation,
        comparables={
            "items": comparable_items,
            "count": comparable_count,
            "metrics": comparable_metrics,
        },
        growth=growth,
    )

    if not isinstance(risk, dict):
        risk = {}

    # ---------------------------------------------------------
    # CRITICAL FIX
    #
    # Inject the freshly calculated risk result into intelligence.
    #
    # InvestmentEngine reads:
    #
    #     intelligence["risk"]
    #
    # therefore it must see the calculated risk result.
    # ---------------------------------------------------------

    intelligence["risk"] = risk

    # ---------------------------------------------------------
    # Keep infrastructure synchronized as well.
    #
    # This protects against build_property_intelligence() returning
    # stale or incomplete infrastructure data.
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    # ---------------------------------------------------------
    # Synchronize calculated intelligence
    #
    # The individual engines return:
    #
    # infrastructure -> infrastructure_score
    # growth         -> score
    # risk           -> score
    # valuation      -> available / estimated_value / etc.
    #
    # InvestmentEngine expects infrastructure["score"],
    # growth["score"], and risk["score"].
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    # Infrastructure
    # ---------------------------------------------------------

    intelligence_infrastructure = intelligence.get(
        "infrastructure",
        {},
    )

    if not isinstance(intelligence_infrastructure, dict):
        intelligence_infrastructure = {}

    infrastructure_score = infrastructure.get(
        "infrastructure_score"
    )

    if infrastructure_score is None:
        infrastructure_score = infrastructure.get(
            "score"
        )

    if infrastructure_score is not None:
        intelligence_infrastructure["score"] = (
            infrastructure_score
        )

        intelligence_infrastructure[
            "infrastructure_score"
        ] = infrastructure_score

    # Preserve all infrastructure engine data.
    for key, value in infrastructure.items():
        intelligence_infrastructure[key] = value

    # Re-apply normalized score because the engine data may
    # contain infrastructure_score rather than score.
    if infrastructure_score is not None:
        intelligence_infrastructure["score"] = (
            infrastructure_score
        )

        intelligence_infrastructure[
            "infrastructure_score"
        ] = infrastructure_score

    intelligence["infrastructure"] = (
        intelligence_infrastructure
    )

    # ---------------------------------------------------------
    # Growth
    # ---------------------------------------------------------

    intelligence["growth"] = growth

    # ---------------------------------------------------------
    # Risk
    #
    # Risk is calculated immediately after this block, so this
    # assignment should happen again after risk_engine returns.
    # ---------------------------------------------------------



    # ---------------------------------------------------------
    # Keep pricing synchronized with comparable metrics.
    #
    # Only update fields that can safely be derived from the
    # comparable engine. Do not invent target price/area.
    # ---------------------------------------------------------

    pricing = intelligence.get(
        "pricing",
        {},
    )

    if not isinstance(pricing, dict):
        pricing = {}

    pricing["comparable_count"] = comparable_count

    pricing["priced_comparables"] = (
        comparable_metrics.get(
            "priced_comparables",
            comparable_count,
        )
    )

    pricing["average_price"] = comparable_metrics.get(
        "average_price",
        pricing.get("average_price"),
    )

    pricing["median_price"] = comparable_metrics.get(
        "median_price",
        pricing.get("median_price"),
    )

    pricing["average_price_per_area"] = comparable_metrics.get(
        "average_price_per_area",
        pricing.get("average_price_per_area"),
    )

    pricing["price_range"] = comparable_metrics.get(
        "price_range",
        pricing.get("price_range"),
    )

    # These MUST remain based on the actual target property.
    pricing["target_price_available"] = (
        property_item.price is not None
    )

    pricing["target_area_available"] = (
        property_item.area is not None
    )

    pricing["target_price"] = property_item.price
    pricing["target_currency"] = property_item.currency

    intelligence["pricing"] = pricing

    # ---------------------------------------------------------
    # Evidence confidence
    #
    # This measures availability/reliability of the current
    # infrastructure and comparable evidence.
    #
    # It is NOT the final investment confidence score.
    # ---------------------------------------------------------

    infrastructure_confidence = infrastructure.get(
        "confidence",
        0.0,
    )

    if infrastructure_confidence is None:
        infrastructure_confidence = 0.0

    infrastructure_confidence = float(
        infrastructure_confidence
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

    investment = investment_engine.assess(
        property_data=target,
        intelligence=intelligence,
        valuation=valuation,
        comparables={
            "items": comparable_items,
            "count": comparable_count,
            "metrics": comparable_metrics,
        },
    )

    if not isinstance(investment, dict):
        investment = {}

    deal = deal_engine.assess(
        property_data=target,
        investment=investment,
        valuation=valuation,
        growth=growth,
        risk=risk,
        intelligence=intelligence,
        comparables={
            "items": comparable_items,
            "count": comparable_count,
            "metrics": comparable_metrics,
        },
    )


    personalization = personalization_engine.assess(
        property_data=target,
        investment=investment,
        investor_profile=investor_profile or {},
    )

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    return {
        "property_found": True,

        "property": {
            "id": property_item.id,
            "title": property_item.title,
            "project_name": property_item.project_name,
            "developer": property_item.developer,
            "source": property_item.source,
            "property_type": property_item.property_type,
            "listing_type": property_item.listing_type,
            "country": property_item.country,
            "city": property_item.city,
            "location": property_item.location,
            "price": property_item.price,
            "currency": property_item.currency,
            "bedrooms": property_item.bedrooms,
            "bathrooms": property_item.bathrooms,
            "area": property_item.area,
            "area_unit": property_item.area_unit,
            "status": property_item.status,
            "completion_date": property_item.completion_date,
            "brands": property_item.brands,
            "source_url": property_item.source_url,
        },

        "location": location,

        "infrastructure": infrastructure,

        "comparables": {
            "items": comparable_items,
            "count": comparable_count,
            "metrics": comparable_metrics,
        },

        # IMPORTANT:
        # intelligence now contains the actual calculated
        # infrastructure, pricing, growth and risk values.
        "intelligence": intelligence,

        "valuation": valuation,

        "growth": growth,

        "risk": risk,

        "investment": investment,

        "deal": deal,
        
        "personalization": personalization,

        "confidence": round(
            confidence,
            2,
        ),
    }

