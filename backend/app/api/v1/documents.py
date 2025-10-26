"""Endpoint tra cứu văn bản."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import models
from ...db.base import get_session
from ...schemas.document import Document, DocumentSearchResult
from ...services.repository import DocumentRepository

router = APIRouter()


@router.get("", response_model=DocumentSearchResult)
async def list_documents(
    keyword: str | None = Query(default=None, description="Từ khoá tìm kiếm"),
    ma_hs: str | None = Query(default=None, description="Mã HS chính xác"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> DocumentSearchResult:
    """Trả về danh sách văn bản theo điều kiện lọc."""

    repository = DocumentRepository(session)
    total, items = await repository.search_documents(
        keyword=keyword, ma_hs=ma_hs, limit=limit, offset=offset
    )
    return DocumentSearchResult(
        total=total,
        items=[Document.model_validate(item) for item in items],
    )


@router.get("/{document_id}", response_model=Document)
async def get_document(document_id: int, session: AsyncSession = Depends(get_session)) -> Document:
    """Lấy thông tin chi tiết của một văn bản."""

    document = await session.get(models.Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy văn bản")
    return Document.model_validate(document)
