from __future__ import annotations

import os
from typing import Any

import requests


class OpenRouterClient:
    """
    Thin client around the OpenRouter API.

    Uses the OpenAI-compatible chat completions endpoint.
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout: int = 120,
    ) -> None:

        self.api_key = (
            api_key
            or os.getenv("OPENROUTER_API_KEY")
        )

        self.model = (
            model
            or os.getenv(
                "OPENROUTER_MODEL",
                "openrouter/free",
            )
        )

        self.timeout = timeout

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable "
                "is not configured"
            )

    def generate(
        self,
        prompt: str,
        system: str | None = None,
    ) -> str:

        messages: list[dict[str, str]] = []

        if system:
            messages.append(
                {
                    "role": "system",
                    "content": system,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        try:
            answer = data["choices"][0]["message"]["content"]
        except (
            KeyError,
            IndexError,
            TypeError,
        ) as exc:
            raise ValueError(
                f"Unexpected OpenRouter response: {data}"
            ) from exc

        if not answer:
            raise ValueError(
                "OpenRouter returned an empty response"
            )

        return answer
