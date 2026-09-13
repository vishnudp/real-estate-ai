from __future__ import annotations

import json
import os
from typing import Any

import requests


class OllamaClient:
    """
    Thin client around the local Ollama HTTP API.

    The client is responsible only for communicating with Ollama.
    Business logic and investment calculations stay outside this class.
    """

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = 120,
    ) -> None:

        self.base_url = (
            base_url
            or os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434",
            )
        ).rstrip("/")

        self.model = (
            model
            or os.getenv(
                "OLLAMA_MODEL",
                "qwen3:4b",
            )
        )

        self.timeout = timeout

    def generate(
        self,
        prompt: str,
        system: str | None = None,
    ) -> str:

        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": 2048,
                "num_predict": 300,
            },
        }

        if system:
            payload["system"] = system

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "response",
            "",
        )

        if not answer:
            raise ValueError(
                "Ollama returned an empty response"
            )

        return answer


    def generate_json(
        self,
        prompt: str,
        schema: dict[str, Any],
        system: str | None = None,
    ) -> dict[str, Any]:

        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "format": schema,
            "options": {
                "num_ctx": 2048,
                "num_predict": 512,
            },
        }

        if system:
            payload["system"] = system

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        raw_response = data.get(
            "response",
            "",
        )

        if not raw_response:
            raise ValueError(
                "Ollama returned an empty response"
            )

        try:
            parsed = json.loads(
                raw_response
            )

        except json.JSONDecodeError as exc:

            raise ValueError(
                "Ollama returned invalid JSON"
            ) from exc

        if not isinstance(parsed, dict):

            raise ValueError(
                "Ollama JSON response must be an object"
            )

        return parsed


ollama_client = OllamaClient()