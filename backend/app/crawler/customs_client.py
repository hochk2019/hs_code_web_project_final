"""Client thu thập dữ liệu từ cổng thông tin Hải quan Việt Nam."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

LIST_ENDPOINT = "https://www.customs.gov.vn/index.jsp"
DETAIL_ENDPOINT = "https://www.customs.gov.vn/index.jsp"


@dataclass(slots=True)
class CustomsDocument:
    """Đại diện cho một văn bản trên cổng thông tin Hải quan."""

    so_ky_hieu: str
    tieu_de: str
    ngay_ban_hanh: Optional[datetime]
    detail_url: str


class CustomsClient:
    """Xử lý việc gọi HTTP và phân tích HTML."""

    def __init__(self, timeout: float = 15.0):
        self._client = httpx.AsyncClient(timeout=timeout)

    async def close(self) -> None:
        await self._client.aclose()

    @retry(wait=wait_exponential(multiplier=1, min=2, max=30), stop=stop_after_attempt(5))
    async def fetch_list(
        self,
        *,
        page: int = 1,
        linh_vuc: int = 313,
    ) -> Iterable[CustomsDocument]:
        """Lấy danh sách văn bản phân trang."""

        params = {"pageId": 8, "cid": 1294, "page": page, "LinhVuc": linh_vuc}
        response = await self._client.get(LIST_ENDPOINT, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        for row in soup.select(".ketqua-phanloaivb ul li"):
            link = row.select_one("a")
            date_str = row.select_one("span")
            if not link:
                continue
            so_ky_hieu = link.text.strip()
            detail_url = httpx.URL(link.get("href", ""), base=LIST_ENDPOINT).resolve().human_repr()
            ngay_ban_hanh = None
            if date_str:
                try:
                    ngay_ban_hanh = datetime.strptime(date_str.text.strip(), "%d/%m/%Y")
                except ValueError:
                    ngay_ban_hanh = None
            yield CustomsDocument(
                so_ky_hieu=so_ky_hieu,
                tieu_de=link.get("title", so_ky_hieu),
                ngay_ban_hanh=ngay_ban_hanh,
                detail_url=detail_url,
            )

    @retry(wait=wait_exponential(multiplier=1, min=2, max=30), stop=stop_after_attempt(5))
    async def fetch_detail(self, detail_url: str) -> dict[str, str | None]:
        """Tải trang chi tiết và bóc tách các trường dữ liệu thô."""

        response = await self._client.get(detail_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        result: dict[str, str | None] = {}

        for row in soup.select("table.table tr"):
            columns = row.find_all("td")
            if len(columns) < 2:
                continue
            key = columns[0].get_text(strip=True)
            value = columns[1].get_text(strip=True)
            result[key] = value or None

        link = soup.find("a", string=lambda text: text and "pdf" in text.lower())
        if link:
            result["pdf_url"] = httpx.URL(link.get("href", ""), base=detail_url).resolve().human_repr()
        return result
