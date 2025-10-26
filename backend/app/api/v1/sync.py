"""Endpoint kích hoạt đồng bộ dữ liệu."""

from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


async def run_sync_job() -> None:
    """Placeholder cho tác vụ đồng bộ dữ liệu."""

    # TODO: tích hợp crawler + pipeline + lưu DB
    return None


@router.post("/run", summary="Kích hoạt đồng bộ ngay")
async def trigger_sync(background_tasks: BackgroundTasks) -> dict[str, str]:
    background_tasks.add_task(run_sync_job)
    return {"status": "accepted"}
