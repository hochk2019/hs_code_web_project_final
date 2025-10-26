"""Cấu hình ứng dụng backend."""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Định nghĩa cấu hình toàn cục cho dịch vụ."""

    app_name: str = Field(default="HS Code Service", description="Tên hiển thị của ứng dụng")
    debug: bool = Field(default=False, description="Bật chế độ gỡ lỗi FastAPI")
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/hs_code",
        description="Chuỗi kết nối PostgreSQL ở dạng async SQLAlchemy",
    )
    allowed_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        description="Danh sách origin được phép truy cập API",
    )
    ai_providers: List[str] = Field(
        default_factory=lambda: ["openrouter", "agentrouter", "ollama"],
        description="Danh sách nhà cung cấp AI khả dụng",
    )
    storage_dir: str = Field(default="storage/raw", description="Thư mục lưu trữ PDF gốc")
    timezone: str = Field(default="Asia/Ho_Chi_Minh", description="Múi giờ mặc định")
    scheduler_enabled: bool = Field(default=True, description="Bật lịch đồng bộ dữ liệu tự động")
    sync_interval_minutes: int = Field(default=360, description="Chu kỳ đồng bộ dữ liệu (phút)")
    openrouter_api_key: Optional[str] = Field(default=None, description="API key OpenRouter")
    agentrouter_api_key: Optional[str] = Field(default=None, description="API key AgentRouter")
    ollama_endpoint: Optional[str] = Field(
        default=None, description="Địa chỉ máy chủ Ollama nội bộ"
    )

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    """Trả về singleton Settings."""

    return Settings()


settings = get_settings()
