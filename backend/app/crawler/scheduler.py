"""Thiết lập lịch đồng bộ dữ liệu định kỳ."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Awaitable, Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..config import settings


@asynccontextmanager
def scheduler_context() -> Awaitable[AsyncIOScheduler]:
    """Tạo scheduler với cấu hình từ settings."""

    scheduler = AsyncIOScheduler(timezone=settings.timezone)
    scheduler.start()
    try:
        yield scheduler
    finally:
        scheduler.shutdown(wait=False)


def register_periodic_job(
    scheduler: AsyncIOScheduler,
    func: Callable[..., Awaitable[None]],
    *,
    minutes: int | None = None,
) -> None:
    """Đăng ký tác vụ chạy theo chu kỳ phút."""

    interval = minutes or settings.sync_interval_minutes
    scheduler.add_job(func, "interval", minutes=interval, id="sync-job", replace_existing=True)
