import json
from pathlib import Path

from backend.app.services.normalizer import normalize_record


ROOT = Path(__file__).resolve().parents[2]

INPUT_FILES = [
    ROOT / "scraper" / "darglobal" / "output" / "darglobal_raw.json",
    ROOT / "scraper" / "wasalt" / "output" / "wasalt_raw.json",
]

OUTPUT_DIR = ROOT / "data" / "normalized"
OUTPUT_FILE = OUTPUT_DIR / "properties.json"


def load_records(path: Path):
    if not path.exists():
        print(f"Skipping missing file: {path}")
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data

    return [data]


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    normalized = []
    skipped = 0

    for input_file in INPUT_FILES:
        print(f"\nReading: {input_file}")

        for record in load_records(input_file):
            result = normalize_record(record)

            if result is None:
                skipped += 1
                continue

            normalized.append(result)

    # Basic URL-based deduplication
    unique = {}

    for record in normalized:
        url = record.get("source_url")

        if url:
            unique[url] = record

    normalized = list(unique.values())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            normalized,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("\n================================")
    print("Normalization complete")
    print("================================")
    print(f"Valid records : {len(normalized)}")
    print(f"Skipped       : {skipped}")
    print(f"Output        : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
