from sqlalchemy.orm import Session

from app.models.infrastructure import Infrastructure


INFRASTRUCTURE_DATA = [
    {
        "name": "Muscat International Airport",
        "infrastructure_type": "airport",
        "country": "Oman",
        "city": "Muscat",
        "area": "Seeb",
        "latitude": 23.5937,
        "longitude": 58.2844,
        "importance": 1.0,
        "description": "Main international airport serving Muscat and Oman.",
        "source": "manual",
    },
    {
        "name": "Sultan Qaboos University Hospital",
        "infrastructure_type": "hospital",
        "country": "Oman",
        "city": "Muscat",
        "area": "Al Khoudh",
        "latitude": 23.5889,
        "longitude": 58.1677,
        "importance": 0.9,
        "description": "Major hospital and healthcare facility in Muscat.",
        "source": "manual",
    },
    {
        "name": "Sultan Qaboos University",
        "infrastructure_type": "school",
        "country": "Oman",
        "city": "Muscat",
        "area": "Al Khoudh",
        "latitude": 23.5846,
        "longitude": 58.1664,
        "importance": 0.8,
        "description": "Major university and education institution.",
        "source": "manual",
    },
    {
        "name": "Mall of Oman",
        "infrastructure_type": "shopping",
        "country": "Oman",
        "city": "Muscat",
        "area": "Bausher",
        "latitude": 23.5744,
        "longitude": 58.3981,
        "importance": 0.8,
        "description": "Major shopping and lifestyle destination in Muscat.",
        "source": "manual",
    },
    {
        "name": "Muscat Expressway",
        "infrastructure_type": "road",
        "country": "Oman",
        "city": "Muscat",
        "area": None,
        "latitude": 23.5900,
        "longitude": 58.3500,
        "importance": 0.9,
        "description": "Major road infrastructure connecting areas of Muscat.",
        "source": "manual",
    },
    {
        "name": "Mutrah Corniche",
        "infrastructure_type": "tourism",
        "country": "Oman",
        "city": "Muscat",
        "area": "Mutrah",
        "latitude": 23.6200,
        "longitude": 58.5600,
        "importance": 0.7,
        "description": "Major waterfront tourism and lifestyle destination.",
        "source": "manual",
    },
]


def ingest_infrastructure(
    db: Session,
) -> int:
    """
    Insert infrastructure records if they do not already exist.
    """

    inserted = 0

    for item in INFRASTRUCTURE_DATA:
        existing = (
            db.query(Infrastructure)
            .filter(
                Infrastructure.name == item["name"],
                Infrastructure.infrastructure_type
                == item["infrastructure_type"],
                Infrastructure.city == item["city"],
            )
            .first()
        )

        if existing:
            continue

        infrastructure = Infrastructure(
            **item,
        )

        db.add(infrastructure)
        inserted += 1

    db.commit()

    return inserted
