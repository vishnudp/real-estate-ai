from abc import ABC, abstractmethod
from typing import Any


class BaseScraper(ABC):

    source: str = ""

    @abstractmethod
    async def scrape(self) -> list[dict[str, Any]]:
        """
        Return normalized property/project records.
        """
        raise NotImplementedError

    def normalize_text(self, value: str | None) -> str | None:
        if not value:
            return None

        return " ".join(value.split()).strip()
