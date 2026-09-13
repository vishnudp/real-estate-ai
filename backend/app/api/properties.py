from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.property import Property
from app.schemas.property import PropertyResponse
from app.services.property_analysis import analyze_property
from app.services.ai_orchestrator import ai_orchestrator


router = APIRouter(
    prefix="/api/properties",
    tags=["properties"],
)


@router.get("", response_model=list[PropertyResponse])
def get_properties(
    source: str | None = None,
    city: str | None = None,
    listing_type: str | None = None,
    property_type: str | None = None,
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Property)

    if source:
        query = query.filter(
            Property.source == source
        )

    if city:
        query = query.filter(
            Property.city.ilike(f"%{city}%")
        )

    if listing_type:
        query = query.filter(
            Property.listing_type == listing_type
        )

    if property_type:
        query = query.filter(
            Property.property_type == property_type
        )

    return query.limit(limit).all()


@router.get(
    "/{property_id}",
    response_model=PropertyResponse,
)
def get_property(
    property_id: int,
    db: Session = Depends(get_db),
):
    property_item = (
        db.query(Property)
        .filter(Property.id == property_id)
        .first()
    )

    if not property_item:
        raise HTTPException(
            status_code=404,
            detail="Property not found",
        )

    return property_item


@router.get("/{property_id}/analysis")
def get_property_analysis(
    property_id: int,
    db: Session = Depends(get_db),
):
    return analyze_property(
        db=db,
        property_id=property_id,
    )


@router.post("/{property_id}/ai")
def get_property_ai(
    property_id: int,
    request: dict,
    db: Session = Depends(get_db),
):
    query = request.get("query", "").strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query is required",
        )

    # Make sure the property exists before running analysis.
    property_item = (
        db.query(Property)
        .filter(Property.id == property_id)
        .first()
    )

    if not property_item:
        raise HTTPException(
            status_code=404,
            detail="Property not found",
        )

    # Deterministic property intelligence.
    result = analyze_property(
        db=db,
        property_id=property_id,
    )

    # AI explains the deterministic intelligence.
    return ai_orchestrator.answer(
        query=query,
        result=result,
    )
