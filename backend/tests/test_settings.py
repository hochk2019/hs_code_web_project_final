"""Kiểm tra cấu hình mặc định."""

from app.config import get_settings


def test_settings_defaults() -> None:
    settings = get_settings()
    assert settings.app_name == "HS Code Service"
    assert settings.database_url.startswith("postgresql+asyncpg")
    assert "http://localhost:3000" in settings.allowed_origins
