"""Các endpoint kiểm tra sức khoẻ dịch vụ."""

from fastapi import APIRouter

from ...config import settings

router = APIRouter()


@router.get("/health", summary="Kiểm tra trạng thái dịch vụ")
def health_check() -> dict[str, str]:
    """Trả về thông tin cơ bản xác nhận dịch vụ đang hoạt động."""

    return {"status": "ok", "service": settings.app_name}
