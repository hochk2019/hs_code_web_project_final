"""Chuẩn hóa dữ liệu trích xuất từ AI."""

from __future__ import annotations

import re
from typing import Any, Dict

HS_PATTERN = re.compile(r"\b(\d{2})(\d{2})(\d{2})(\d{2})?\b")


class PostProcessor:
    """Xử lý kết quả từ AI để phù hợp với schema."""

    def normalize_hs_code(self, value: str | None) -> str | None:
        if not value:
            return None
        match = HS_PATTERN.search(value)
        if not match:
            return value.strip()
        groups = [match.group(i) for i in range(1, 5) if match.group(i)]
        return ".".join(groups)

    def sanitize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Làm sạch dữ liệu và đảm bảo unicode hợp lệ."""

        normalized = payload.copy()
        normalized["ma_hs"] = self.normalize_hs_code(payload.get("ma_hs"))
        if "ten_hang" in normalized and normalized["ten_hang"]:
            normalized["ten_hang"] = normalized["ten_hang"].strip()
        if "mo_ta_hang" in normalized and normalized["mo_ta_hang"]:
            normalized["mo_ta_hang"] = normalized["mo_ta_hang"].strip()
        return normalized
