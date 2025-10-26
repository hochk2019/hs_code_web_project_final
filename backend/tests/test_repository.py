"""Kiểm tra DocumentRepository với SQLite trong bộ nhớ."""

import asyncio
from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import models
from app.services.repository import DocumentRepository


@pytest.fixture(scope="module")
async def session_factory():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield factory
    await engine.dispose()


@pytest.mark.asyncio
async def test_upsert_and_search(session_factory):
    async with session_factory() as session:
        repo = DocumentRepository(session)
        await repo.upsert_document(
            so_ky_hieu="30659/CHQ-NVTHQ",
            ten_hang="Máy in 3D",
            mo_ta_hang="Thiết bị in 3D sử dụng công nghệ FDM",
            ma_hs="8477.80.39",
            ngay_ban_hanh=datetime(2024, 5, 1),
            co_quan_ban_hanh="Tổng cục Hải quan",
            nguon_pdf="https://files.customs.gov.vn/VB_30659.pdf",
        )
        await session.commit()

    async with session_factory() as session:
        repo = DocumentRepository(session)
        total, items = await repo.search_documents(keyword="máy in")
        assert total == 1
        assert items[0].ma_hs == "8477.80.39"
