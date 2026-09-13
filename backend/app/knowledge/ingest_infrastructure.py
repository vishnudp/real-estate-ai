from app.db.database import SessionLocal
from app.services.infrastructure_ingestion import (
    ingest_infrastructure,
)


def main():
    db = SessionLocal()

    try:
        inserted = ingest_infrastructure(db)

        print(
            f"INGESTED INFRASTRUCTURE: {inserted}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()
