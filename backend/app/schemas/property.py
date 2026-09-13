from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PropertyBase(BaseModel):
    source: str
    external_id: str | None = None

    title: str
    project_name: str | None = None
    developer: str | None = None

    listing_type: str | None = None
    property_type: str | None = None

    country: str | None = None
    city: str | None = None
    location: str | None = None

    price: float | None = None
    currency: str | None = None

    bedrooms: int | None = None
    bathrooms: int | None = None

    area: float | None = None
    area_unit: str | None = None

    status: str | None = None
    completion_date: str | None = None

    description: str | None = None

    amenities: list[str] | None = None
    brands: list[str] | None = None
    images: list[str] | None = None

    source_url: str
    raw_content: str | None = None

    latitude: float | None = None
    longitude: float | None = None



class PropertyResponse(PropertyBase):
    id: int
    scraped_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str
    intent: str
    filters: dict
    results: list[dict]
    semantic_results: list[dict]
    analysis: list[dict]
    investment: list[dict] = []