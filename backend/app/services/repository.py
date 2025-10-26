"""Lớp truy cập dữ liệu cho tài liệu và kết quả phân tích."""

from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import models


class DocumentRepository:
    """Các thao tác cơ bản với bảng documents và classifications."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_document(
        self,
        so_ky_hieu: str,
        ten_hang: str | None = None,
        mo_ta_hang: str | None = None,
        ma_hs: str | None = None,
        ngay_ban_hanh: datetime | None = None,
        co_quan_ban_hanh: str | None = None,
        nguon_pdf: str | None = None,
        tep_noi_bo: str | None = None,
    ) -> models.Document:
        """Tạo mới hoặc cập nhật văn bản dựa trên số ký hiệu."""

        result = await self.session.execute(
            select(models.Document).where(models.Document.so_ky_hieu == so_ky_hieu)
        )
        document = result.scalar_one_or_none()

        if document is None:
            document = models.Document(so_ky_hieu=so_ky_hieu)
            self.session.add(document)

        document.ten_hang = ten_hang
        document.mo_ta_hang = mo_ta_hang
        document.ma_hs = ma_hs
        document.ngay_ban_hanh = ngay_ban_hanh
        document.co_quan_ban_hanh = co_quan_ban_hanh
        document.nguon_pdf = nguon_pdf
        document.tep_noi_bo = tep_noi_bo
        document.da_xu_ly = ma_hs is not None

        await self.session.flush()
        return document

    async def save_classifications(
        self, document: models.Document, entries: Sequence[tuple[str, str | None, int | None]]
    ) -> None:
        """Lưu danh sách trường thông tin cho một văn bản."""

        document.classifications.clear()
        for truong, gia_tri, thu_tu in entries:
            document.classifications.append(
                models.Classification(
                    truong_thong_tin=truong,
                    gia_tri=gia_tri,
                    thu_tu=thu_tu,
                )
            )
        await self.session.flush()

    async def search_documents(
        self,
        keyword: str | None = None,
        ma_hs: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[int, list[models.Document]]:
        """Tìm kiếm văn bản theo từ khoá hoặc mã HS."""

        query = select(models.Document)
        count_query = select(func.count(models.Document.id))

        if keyword:
            like_pattern = f"%{keyword}%"
            query = query.where(
                func.lower(models.Document.mo_ta_hang).like(func.lower(like_pattern))
                | func.lower(models.Document.ten_hang).like(func.lower(like_pattern))
            )
            count_query = count_query.where(
                func.lower(models.Document.mo_ta_hang).like(func.lower(like_pattern))
                | func.lower(models.Document.ten_hang).like(func.lower(like_pattern))
            )

        if ma_hs:
            query = query.where(models.Document.ma_hs == ma_hs)
            count_query = count_query.where(models.Document.ma_hs == ma_hs)

        total = await self.session.scalar(count_query)
        results = await self.session.execute(
            query.order_by(models.Document.ngay_ban_hanh.desc().nullslast())
            .limit(limit)
            .offset(offset)
        )
        return total or 0, list(results.scalars().all())
