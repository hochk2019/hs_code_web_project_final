"""Router gọi các nhà cung cấp AI."""

from __future__ import annotations

from typing import Any, Dict

import httpx

from ..config import settings


class AIRouterError(RuntimeError):
    """Lỗi khi gọi nhà cung cấp AI."""


class AIRouter:
    """Gửi prompt tới nhà cung cấp phù hợp dựa trên cấu hình."""

    def __init__(self) -> None:
        self.session = httpx.AsyncClient(timeout=60.0)

    async def close(self) -> None:
        await self.session.aclose()

    async def extract_fields(self, text: str) -> Dict[str, Any]:
        """Gọi AI để trích xuất trường thông tin chuẩn."""

        last_error: Exception | None = None
        for provider in settings.ai_providers:
            try:
                if provider == "openrouter" and settings.openrouter_api_key:
                    return await self._call_openrouter(text)
                if provider == "agentrouter" and settings.agentrouter_api_key:
                    return await self._call_agentrouter(text)
                if provider == "ollama" and settings.ollama_endpoint:
                    return await self._call_ollama(text)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                continue
        raise AIRouterError("Không thể gọi bất kỳ nhà cung cấp AI nào") from last_error

    async def _call_openrouter(self, text: str) -> Dict[str, Any]:
        response = await self.session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
            json={
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [
                    {
                        "role": "system",
                        "content": "Hãy trích xuất thông tin HS code từ văn bản PDF và trả về JSON Unicode.",
                    },
                    {"role": "user", "content": text},
                ],
            },
        )
        response.raise_for_status()
        return response.json()

    async def _call_agentrouter(self, text: str) -> Dict[str, Any]:
        response = await self.session.post(
            "https://api.agentrouter.org/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.agentrouter_api_key}"},
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "Chuẩn hóa dữ liệu HS code tiếng Việt dưới dạng JSON.",
                    },
                    {"role": "user", "content": text},
                ],
            },
        )
        response.raise_for_status()
        return response.json()

    async def _call_ollama(self, text: str) -> Dict[str, Any]:
        response = await self.session.post(
            str(settings.ollama_endpoint) + "/api/generate",
            json={"model": "llama3", "prompt": text, "stream": False},
        )
        response.raise_for_status()
        return response.json()
