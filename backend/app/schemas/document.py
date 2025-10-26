"""Schema Pydantic cho tài liệu phân tích phân loại."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class DocumentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    so_ky_hieu: str = Field(..., description="Số ký hiệu văn bản (ví dụ: 30659/CHQ-NVTHQ)")
    ten_hang: Optional[str] = Field(default=None, description="Tên hàng hoá tiếng Việt")
    mo_ta_hang: Optional[str] = Field(default=None, description="Mô tả chi tiết hàng hoá")
    ma_hs: Optional[str] = Field(default=None, description="Mã HS 2022 được xác định")
    ngay_ban_hanh: Optional[datetime] = Field(default=None, description="Ngày ban hành văn bản")
    co_quan_ban_hanh: Optional[str] = Field(default=None, description="Đơn vị ban hành")
    nguon_pdf: Optional[HttpUrl] = Field(default=None, description="Liên kết tải file PDF gốc")


class Document(DocumentBase):
    id: int = Field(..., description="ID tự tăng trong hệ thống")
    created_at: datetime = Field(..., description="Thời điểm ghi vào hệ thống")
    updated_at: datetime = Field(..., description="Thời điểm cập nhật gần nhất")


class DocumentSearchResult(BaseModel):
    total: int = Field(..., description="Tổng số bản ghi thỏa điều kiện")
    items: list[Document] = Field(..., description="Danh sách kết quả")
