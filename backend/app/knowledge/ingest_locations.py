from app.db.database import Base, SessionLocal, engine

from app.models.property import Property
from app.models.location import Location

from app.services.location_ingestion import ingest_locations


locations = [
    {
        "name": "Muscat International Airport",
        "location_type": "airport",
        "country": "Oman",
        "city": "Muscat",
        "source": "manual",
    },
    {
        "name": "AIDA",
        "location_type": "development",
        "country": "Oman",
        "city": "Muscat",
        "area": "AIDA",
        "source": "darglobal",
    },
    {
        "name": "Muscat",
        "location_type": "city",
        "country": "Oman",
        "city": "Muscat",
        "source": "manual",
    },
]


def main():
    Base.metadata.create_all(
        bind=engine,
    )

    db = SessionLocal()

    try:
        results = ingest_locations(
            db,
            locations,
        )

        print(
            f"INGESTED LOCATIONS: {len(results)}"
        )

        for location in results:
            print(
                location.id,
                location.name,
                location.location_type,
                location.city,
                location.country,
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()
