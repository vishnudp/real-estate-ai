from typing import Any

import httpx
from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper


class WasaltScraper(BaseScraper):

    source = "wasalt"

    BASE_URL = "https://wasalt.sa"

    async def scrape(self) -> list[dict[str, Any]]:
        """
        Phase 1 skeleton.

        Phase 3 will implement:
        1. Public listing discovery
        2. Listing extraction
        3. Pagination where appropriate
        4. Normalization
        5. Deduplication
        """

        async with httpx.AsyncClient(
            timeout=30,
            follow_redirects=True,
        ) as client:

            response = await client.get(self.BASE_URL)
            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser",
            )

        return []
