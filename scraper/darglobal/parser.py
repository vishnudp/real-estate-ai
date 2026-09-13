import re
from typing import List

from bs4 import BeautifulSoup


def clean_text(value: str) -> str:
    if not value:
        return ""

    return re.sub(r"\s+", " ", value).strip()


def extract_text(soup: BeautifulSoup) -> str:
    return clean_text(soup.get_text(" ", strip=True))


def extract_meta(
    soup: BeautifulSoup,
    name: str,
) -> str:
    tag = soup.find("meta", attrs={"name": name})

    if tag and tag.get("content"):
        return clean_text(tag["content"])

    return ""


def extract_meta_property(
    soup: BeautifulSoup,
    property_name: str,
) -> str:
    tag = soup.find(
        "meta",
        attrs={"property": property_name},
    )

    if tag and tag.get("content"):
        return clean_text(tag["content"])

    return ""


def extract_title(soup: BeautifulSoup) -> str:
    if soup.title:
        return clean_text(soup.title.get_text())

    return ""


def extract_description(soup: BeautifulSoup) -> str:
    description = extract_meta(soup, "description")

    if description:
        return description

    return extract_meta_property(
        soup,
        "og:description",
    )


def extract_images(
    soup: BeautifulSoup,
    base_url: str,
) -> List[str]:
    images = []

    for img in soup.find_all("img"):
        src = img.get("src")

        if not src:
            continue

        if src.startswith("//"):
            src = "https:" + src

        elif src.startswith("/"):
            from urllib.parse import urljoin

            src = urljoin(base_url, src)

        if src not in images:
            images.append(src)

    return images[:20]


def extract_project_name(soup: BeautifulSoup) -> str:
    og_title = extract_meta_property(
        soup,
        "og:title",
    )

    if og_title:
        return og_title

    return extract_title(soup)
