# Kiến trúc hệ thống tra cứu HS Code

Tài liệu này mô tả kiến trúc tổng thể của nền tảng thu thập và tra cứu kết quả phân tích phân loại hải quan.

## Tổng quan luồng dữ liệu

1. **Crawler** truy xuất danh sách kết quả phân tích phân loại từ cổng thông tin Hải quan.
2. **Download Manager** tải tệp PDF, lưu metadata (mã hồ sơ, ngày ban hành, đường dẫn gốc) vào kho lưu trữ tạm.
3. **Pipeline AI** bóc tách nội dung PDF (bao gồm OCR nếu là bản scan), trích xuất các trường dữ liệu chuẩn (mô tả hàng, mã HS, căn cứ pháp lý, chú giải, hình ảnh) và chuẩn hóa theo HS 2022.
4. **ETL Service** ghi dữ liệu vào PostgreSQL, đồng thời lưu đường dẫn tệp PDF gốc và bản đã xử lý.
5. **Backend API** cung cấp dịch vụ tra cứu, đồng bộ dữ liệu, quản lý lịch sử tải và giám sát.
6. **Frontend Next.js** hiển thị giao diện tiếng Việt cho người dùng tra cứu, tải tài liệu và xuất báo cáo.

## Công nghệ chính

| Tầng | Công nghệ | Ghi chú |
| --- | --- | --- |
| Crawler | Python 3.11, httpx, BeautifulSoup4 | Hỗ trợ phân trang, retry, proxy |
| Xử lý PDF | pdfplumber, pytesseract, Pillow | Tự động chuyển đổi PDF scan sang văn bản |
| AI | OpenRouter / AgentRouter / Ollama | Lựa chọn linh hoạt qua lớp trừu tượng `ai_router` |
| Cơ sở dữ liệu | PostgreSQL 16 | Lưu trữ tài liệu, chỉ mục toàn văn (pg_trgm) |
| Backend API | FastAPI, SQLAlchemy, Pydantic | Kiến trúc service/repository, tuân thủ Unicode |
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS | Giao diện tiếng Việt, hỗ trợ dark mode |
| Triển khai | Docker Compose, GitHub Actions CI | Tương thích Windows 11 + PowerShell 7 |

## Sơ đồ thư mục

```
backend/
  app/
    api/
    crawler/
    db/
    schemas/
    services/
  tests/
frontend/
  app/
  components/
  lib/
  public/
  tests/
infrastructure/
  docker-compose.yml
  run_tests.ps1
```

## Chi tiết thành phần

### Crawler & Scheduler

- `customs_client.py`: lấy danh sách văn bản, phân tích HTML, trả về cấu trúc chuẩn.
- `download_manager.py`: tải PDF, tính checksum SHA256, lưu vào `storage/raw/`.
- `scheduler.py`: sử dụng APScheduler để chạy định kỳ (mặc định mỗi 6 giờ), ghi log vào bảng `sync_log`.

### Pipeline AI

- `pdf_extractor.py`: xử lý PDF thành văn bản, nhận diện bảng biểu.
- `ai_router.py`: lựa chọn nhà cung cấp AI, cân bằng tải giữa OpenRouter/AgentRouter/Ollama.
- `postprocessor.py`: chuẩn hóa kết quả, ghép chú giải HS 2022 và phân loại độ tin cậy.

### Tầng dữ liệu

- PostgreSQL với schema `public` chứa các bảng `documents`, `classifications`, `commodities`, `sync_log`.
- Sử dụng Alembic để quản lý migration.
- Tích hợp Elasticsearch hoặc pgvector (tuỳ chọn) để tăng tốc tìm kiếm nâng cao.

### Backend API

- FastAPI cung cấp các route `GET /documents`, `GET /documents/{id}`, `POST /sync/run`, `GET /health`.
- Sử dụng OAuth2 (Keycloak hoặc Azure AD) cho quản trị viên (phần mở rộng tương lai).
- OpenAPI tự động tạo từ FastAPI, hỗ trợ tiếng Việt.

### Frontend

- Form tìm kiếm (tên hàng, mô tả, mã HS, thời gian ban hành).
- Trang danh sách với phân trang, bộ lọc nhanh, highlight từ khoá.
- Trang chi tiết hiển thị thông tin đầy đủ, link tải PDF gốc và bản đã chuẩn hóa.
- Module quản trị (tùy chọn) để theo dõi trạng thái đồng bộ và pipeline AI.

### Giám sát & Logging

- Sử dụng structlog + log JSON.
- Docker Compose tích hợp Prometheus & Grafana (cấu hình bổ sung sau).
- Alerting qua webhook/Email khi pipeline gặp lỗi.

## Lộ trình phát triển

1. Hoàn thiện skeleton backend/frontend, Docker Compose, CI.
2. Xây dựng crawler & lưu metadata vào DB.
3. Tích hợp pipeline AI và OCR.
4. Hoàn thiện API tra cứu, phân quyền cơ bản.
5. Phát triển giao diện người dùng hoàn chỉnh, thêm tính năng xuất báo cáo.
6. Tối ưu hoá hiệu năng, cache, và giám sát.
