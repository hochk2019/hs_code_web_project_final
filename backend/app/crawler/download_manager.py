"""Quản lý tải xuống và lưu trữ PDF."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional

import httpx

from ..config import settings


class DownloadResult(dict):
    """Kết quả trả về sau khi tải tệp."""

    path: Path
    checksum: str


class DownloadManager:
    """Tải và lưu các tệp PDF từ nguồn Hải quan."""

    def __init__(self, storage_dir: str | None = None):
        self.storage_path = Path(storage_dir or settings.storage_dir)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    async def download(self, url: str, *, filename: Optional[str] = None) -> Path:
        """Tải tệp PDF và lưu trữ, trả về đường dẫn nội bộ."""

        target_name = filename or url.split("/")[-1] or "document.pdf"
        destination = self.storage_path / target_name

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            destination.write_bytes(response.content)

        return destination

    @staticmethod
    def checksum(path: Path, algorithm: str = "sha256") -> str:
        """Tính checksum cho tệp đã tải."""

        hash_obj = hashlib.new(algorithm)
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
