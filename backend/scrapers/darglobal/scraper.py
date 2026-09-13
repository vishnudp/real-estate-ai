from typing import Any

import httpx
from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper


class DarGlobalScraper(BaseScraper):

    source = "darglobal"

    BASE_URL = "https://www.darglobal.co.uk"

    async def scrape(self) -> list[dict[str, Any]]:
        """
        Phase 1 skeleton.

        Phase 2 will implement:
        1. robots/terms-aware discovery
        2. project URL collection
        3. public page extraction
        4. normalization
        5. deduplication
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
