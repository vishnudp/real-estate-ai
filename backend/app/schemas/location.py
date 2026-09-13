from pydantic import BaseModel, ConfigDict


class LocationBase(BaseModel):
    name: str
    location_type: str

    country: str | None = None
    city: str | None = None
    area: str | None = None
    address: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    source: str
    source_url: str | None = None


class LocationResponse(LocationBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
