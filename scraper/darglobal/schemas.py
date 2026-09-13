from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DarGlobalProject:
    source: str = "DarGlobal"
    source_url: str = ""

    project_name: str = ""
    description: str = ""

    country: str = ""
    city: str = ""
    location: str = ""

    property_type: str = ""
    status: str = ""
    completion_date: Optional[str] = None

    unit_types: List[str] = field(default_factory=list)
    bedrooms: List[str] = field(default_factory=list)
    area: str = ""

    amenities: List[str] = field(default_factory=list)
    brands: List[str] = field(default_factory=list)

    image_urls: List[str] = field(default_factory=list)

    scraped_at: str = ""
