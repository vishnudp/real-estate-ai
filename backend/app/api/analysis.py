from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.property import Property
from app.services.comparable_engine import (
    calculate_comparable_metrics,
    find_comparables,
)
from app.services.infrastructure_engine import (
    analyze_property_infrastructure,
)


router = APIRouter(
    prefix="/api/properties",
    tags=["property-analysis"],
)


@router.get("/{property_id}/infrastructure")
def property_infrastructure(
    property_id: int,
    db: Session = Depends(get_db),
):
    """
    Analyze infrastructure surrounding a property.
    """

    result = analyze_property_infrastructure(
        db,
        property_id,
    )

    if not result.get("location_found"):
        raise HTTPException(
            status_code=404,
            detail="Property or property location not found",
        )

    return result


@router.get("/{property_id}/comparables")
def property_comparables(
    property_id: int,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Find comparable properties and calculate market metrics.
    """

    if limit < 1 or limit > 50:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 50",
        )

    result = find_comparables(
        db,
        property_id=property_id,
        limit=limit,
    )

    if not result.get("property_found"):
        raise HTTPException(
            status_code=404,
            detail="Property not found",
        )

    metrics = calculate_comparable_metrics(
        result,
    )

    return {
        **result,
        "metrics": metrics,
    }


# @router.get("/{property_id}/analysis")
# def property_analysis(
#     property_id: int,
#     db: Session = Depends(get_db),
# ):
#     """
#     Return combined infrastructure and comparable analysis.
#     """

#     property_item = (
#         db.query(Property)
#         .filter(Property.id == property_id)
#         .first()
#     )

#     if not property_item:
#         raise HTTPException(
#             status_code=404,
#             detail="Property not found",
#         )

#     infrastructure = analyze_property_infrastructure(
#         db,
#         property_id,
#     )

#     comparables = find_comparables(
#         db,
#         property_id=property_id,
#         limit=10,
#     )

#     comparable_metrics = calculate_comparable_metrics(
#         comparables,
#     )

#     return {
#         "property": {
#             "id": property_item.id,
#             "title": property_item.title,
#             "project_name": property_item.project_name,
#             "developer": property_item.developer,
#             "property_type": property_item.property_type,
#             "city": property_item.city,
#             "country": property_item.country,
#             "price": property_item.price,
#             "currency": property_item.currency,
#             "bedrooms": property_item.bedrooms,
#             "bathrooms": property_item.bathrooms,
#             "area": property_item.area,
#             "area_unit": property_item.area_unit,
#         },
#         "infrastructure": infrastructure,
#         "comparables": comparables,
#         "comparable_metrics": comparable_metrics,
#     }
