import json
from collections import Counter


PATH = "data/normalized/properties.json"


def main():
    with open(PATH, "r", encoding="utf-8") as f:
        records = json.load(f)

    print("=" * 80)
    print("NORMALIZATION QUALITY REPORT")
    print("=" * 80)

    print(f"\nTotal records: {len(records)}")

    # --------------------------------------------------------
    # Document types
    # --------------------------------------------------------

    document_types = Counter(
        r.get("document_type")
        for r in records
    )

    print("\nDocument types")
    print("-" * 40)

    for document_type, count in sorted(
        document_types.items()
    ):
        print(
            f"{document_type:20} {count}"
        )

    # --------------------------------------------------------
    # Property records
    # --------------------------------------------------------

    properties = [
        r
        for r in records
        if r.get("document_type") == "property"
    ]

    print("\nProperty records")
    print("-" * 40)
    print(f"Total properties: {len(properties)}")

    if not properties:
        print("\nNo property records found.")
        return

    # --------------------------------------------------------
    # Metadata coverage
    # --------------------------------------------------------

    fields = [
        "property_name",
        "developer",
        "brand",
        "country",
        "city",
        "location",
        "property_type",
        "investment",
        "investment_type",
        "price",
        "bedrooms",
        "area",
    ]

    print("\nMetadata coverage")
    print("-" * 40)

    for field in fields:
        populated = sum(
            1
            for r in properties
            if r.get(field) not in (
                None,
                "",
                [],
            )
        )

        total = len(properties)

        percentage = (
            populated / total * 100
            if total
            else 0
        )

        print(
            f"{field:20} "
            f"{populated:3}/{total:<3} "
            f"({percentage:5.1f}%)"
        )

    # --------------------------------------------------------
    # Property details
    # --------------------------------------------------------

    print("\nProperty details")
    print("-" * 80)

    for i, r in enumerate(properties, 1):

        print(f"\n[{i}] {r.get('property_name')}")
        print(
            f"    Title:        {r.get('title')}"
        )
        print(
            f"    Developer:    {r.get('developer')}"
        )
        print(
            f"    Brand:        {r.get('brand')}"
        )
        print(
            f"    Country:      {r.get('country')}"
        )
        print(
            f"    City:         {r.get('city')}"
        )
        print(
            f"    Location:     {r.get('location')}"
        )
        print(
            f"    Type:         {r.get('property_type')}"
        )
        print(
            f"    Price:        {r.get('price')}"
        )
        print(
            f"    Bedrooms:     {r.get('bedrooms')}"
        )
        print(
            f"    Area:         {r.get('area')}"
        )
        print(
            f"    Investment:   {r.get('investment_type')}"
        )

    # --------------------------------------------------------
    # Price safety check
    # --------------------------------------------------------

    print("\nPrice safety check")
    print("-" * 40)

    non_properties_with_price = [
        r
        for r in records
        if r.get("document_type") != "property"
        and r.get("price") not in (
            None,
            "",
        )
    ]

    if non_properties_with_price:
        print(
            "WARNING: Non-property records "
            "contain prices!"
        )

        for r in non_properties_with_price:
            print(
                f"  {r.get('document_type'):15} "
                f"{r.get('price')} | "
                f"{r.get('source_url')}"
            )
    else:
        print(
            "OK: No non-property records "
            "contain prices."
        )

    # --------------------------------------------------------
    # Duplicate URLs
    # --------------------------------------------------------

    print("\nDuplicate URL check")
    print("-" * 40)

    urls = [
        r.get("source_url")
        for r in records
        if r.get("source_url")
    ]

    duplicates = [
        url
        for url, count in Counter(urls).items()
        if count > 1
    ]

    if duplicates:
        print(
            f"WARNING: {len(duplicates)} "
            "duplicate URLs found."
        )

        for url in duplicates:
            print(f"  {url}")
    else:
        print("OK: No duplicate URLs found.")

    print("\n" + "=" * 80)
    print("REPORT COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
