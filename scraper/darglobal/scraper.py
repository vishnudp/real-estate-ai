import json
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


BASE_URL = "https://darglobal.co.uk"

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_FILE = OUTPUT_DIR / "darglobal_raw.json"

MAX_PAGES = 20

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def is_valid_page(url: str) -> bool:
    parsed = urlparse(url)

    if parsed.netloc not in {
        "darglobal.co.uk",
        "www.darglobal.co.uk",
    }:
        return False

    path = parsed.path.lower()

    # Ignore assets
    ignored_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".svg",
        ".ico",
        ".pdf",
        ".zip",
        ".css",
        ".js",
        ".woff",
        ".woff2",
    )

    if path.endswith(ignored_extensions):
        return False

    return True


def discover_links(page) -> set[str]:
    links = set()

    anchors = page.locator("a[href]").all()

    for anchor in anchors:
        try:
            href = anchor.get_attribute("href")

            if not href:
                continue

            url = urljoin(BASE_URL, href)

            # Remove fragment
            url = url.split("#")[0]

            if is_valid_page(url):
                links.add(url)

        except Exception:
            continue

    return links


def extract_page(page, url: str) -> dict:
    title = ""

    try:
        title = page.title()
    except Exception:
        pass

    html = page.content()

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    description = ""

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"},
    )

    if meta_description:
        description = (
            meta_description.get("content")
            or ""
        )

    # Remove scripts/styles
    for tag in soup(
        ["script", "style", "noscript"]
    ):
        tag.decompose()

    text = soup.get_text(
        " ",
        strip=True,
    )

    return {
        "source": "darglobal",
        "source_url": url,
        "title": title,
        "description": description,
        "content": text[:30000],
        "scraped_at": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ",
            time.gmtime(),
        ),
    }


def main():
    print("Starting DarGlobal scraper...")
    print(f"Base URL: {BASE_URL}")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    records = []
    visited = set()

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=True,
        )

        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport={
                "width": 1440,
                "height": 900,
            },
        )

        page = context.new_page()

        try:
            print(
                f"Opening {BASE_URL}"
            )

            response = page.goto(
                BASE_URL,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            print(
                f"Initial response: "
                f"{response.status if response else 'unknown'}"
            )

            # Give JavaScript time to render.
            page.wait_for_timeout(5000)

            print(
                f"Loaded title: {page.title()}"
            )

            links = discover_links(page)

            print(
                f"Discovered {len(links)} links"
            )

            # Prioritize likely project/property pages.
            priority_links = []

            for url in links:

                path = urlparse(url).path.lower()

                if any(
                    keyword in path
                    for keyword in (
                        "project",
                        "property",
                        "residence",
                        "development",
                        "dubai",
                        "oman",
                        "saudi",
                        "qatar",
                        "maldives",
                    )
                ):
                    priority_links.append(url)

            # Add remaining links after priority pages.
            ordered_links = (
                priority_links
                + [
                    url
                    for url in sorted(links)
                    if url not in priority_links
                ]
            )

            # Always include homepage.
            ordered_links.insert(
                0,
                BASE_URL,
            )

            # Remove duplicates while preserving order.
            final_links = []

            for url in ordered_links:

                if url not in final_links:
                    final_links.append(url)

            final_links = final_links[:MAX_PAGES]

            print(
                f"Will scrape {len(final_links)} pages"
            )

            for index, url in enumerate(
                final_links,
                start=1,
            ):

                if url in visited:
                    continue

                visited.add(url)

                try:
                    print(
                        f"[{index}/{len(final_links)}] "
                        f"Scraping: {url}"
                    )

                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=60000,
                    )

                    page.wait_for_timeout(2000)

                    record = extract_page(
                        page,
                        url,
                    )

                    # Don't store empty pages.
                    if len(record["content"]) < 100:
                        print(
                            "  Skipped: insufficient content"
                        )
                        continue

                    records.append(record)

                    print(
                        f"  ✓ {record['title']}"
                    )

                    # Keep request rate low.
                    time.sleep(1)

                except Exception as exc:
                    print(
                        f"  ✗ Failed: {exc}"
                    )

        finally:
            browser.close()

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print("=" * 60)
    print(
        f"Saved {len(records)} records"
    )
    print("=" * 60)
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
