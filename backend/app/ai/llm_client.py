from __future__ import annotations

import os
from typing import Any

from app.ai.ollama_client import OllamaClient
from app.ai.openrouter_client import OpenRouterClient


class LLMClient:
    """
    Provider-independent LLM client.

    The provider is selected using:

        LLM_PROVIDER=ollama
        LLM_PROVIDER=openrouter
    """

    def __init__(self) -> None:
        self.provider = os.getenv(
            "LLM_PROVIDER",
            "ollama",
        ).lower().strip()

        if self.provider == "ollama":
            self.client = OllamaClient()

        elif self.provider == "openrouter":
            self.client = OpenRouterClient()

        else:
            raise ValueError(
                f"Unsupported LLM_PROVIDER: {self.provider}. "
                "Expected 'ollama' or 'openrouter'."
            )

    def generate(
        self,
        prompt: str,
        system: str | None = None,
    ) -> str:
        """
        Generate a normal text response.
        """

        return self.client.generate(
            prompt=prompt,
            system=system,
        )

    def generate_json(
        self,
        prompt: str,
        schema: dict[str, Any],
        system: str | None = None,
    ) -> dict[str, Any]:
        """
        Generate a JSON response.

        Ollama supports structured JSON directly.
        OpenRouter currently receives the schema as part of
        the prompt through its client implementation.
        """

        if hasattr(self.client, "generate_json"):
            return self.client.generate_json(
                prompt=prompt,
                schema=schema,
                system=system,
            )

        raise NotImplementedError(
            f"generate_json is not implemented for "
            f"provider '{self.provider}'"
        )


llm_client = LLMClient()
