"""Định nghĩa bảng dữ liệu chính."""

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Lớp cơ sở cho ORM."""

    pass


def utc_now() -> datetime:
    """Trả về thời điểm UTC hiện tại ở dạng timezone-aware."""

    return datetime.now(UTC)


class Document(Base):
    """Bảng lưu thông tin văn bản phân tích phân loại."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    so_ky_hieu: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    ten_hang: Mapped[str | None] = mapped_column(String(500), nullable=True)
    mo_ta_hang: Mapped[str | None] = mapped_column(Text, nullable=True)
    ma_hs: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    ngay_ban_hanh: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    co_quan_ban_hanh: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nguon_pdf: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    tep_noi_bo: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    da_xu_ly: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    classifications: Mapped[list["Classification"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )


class Classification(Base):
    """Bảng lưu chi tiết kết quả phân tích."""

    __tablename__ = "classifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)
    truong_thong_tin: Mapped[str] = mapped_column(String(255), nullable=False)
    gia_tri: Mapped[str | None] = mapped_column(Text, nullable=True)
    thu_tu: Mapped[int | None] = mapped_column(Integer, nullable=True)

    document: Mapped[Document] = relationship(back_populates="classifications")


class SyncLog(Base):
    """Theo dõi lịch sử đồng bộ."""

    __tablename__ = "sync_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bat_dau: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    ket_thuc: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    so_luong_tai: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    thanh_cong: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    thong_diep_loi: Mapped[str | None] = mapped_column(Text, nullable=True)
