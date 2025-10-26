# Hệ thống tra cứu HS Code hải quan Việt Nam

Dự án này nhằm xây dựng một nền tảng thu thập, chuẩn hóa và tra cứu kết quả phân tích phân loại do Tổng cục Hải quan Việt Nam công bố. Hệ thống bao gồm các thành phần crawler, pipeline AI bóc tách dữ liệu từ PDF, API backend, giao diện web tiếng Việt và hạ tầng triển khai hiện đại.

## Thành phần chính

- **backend/** – Dịch vụ FastAPI thu thập dữ liệu, xử lý AI, cung cấp API tra cứu, lưu trữ trên cơ sở dữ liệu quan hệ hiện đại (PostgreSQL).
- **frontend/** – Ứng dụng Next.js tiếng Việt cung cấp giao diện tra cứu HS code, hỗ trợ phân trang và tải tài liệu gốc.
- **docs/** – Tài liệu kiến trúc và hướng dẫn triển khai.
- **infrastructure/** – Cấu hình Docker Compose, script chạy kiểm thử, và tiện ích triển khai.
- **.github/** – Quy trình CI kiểm thử và lint tự động.

## Bắt đầu nhanh

1. Cài đặt Docker và Docker Compose.
2. Chạy `docker compose up --build` để khởi động PostgreSQL, backend và frontend.
3. Truy cập `http://localhost:3000` để sử dụng giao diện tra cứu.
4. Thực thi `./infrastructure/run_tests.ps1` (hoặc tương đương trên Linux/macOS) để chạy toàn bộ kiểm thử và lint.

## Yêu cầu

- Python ≥ 3.11
- Node.js ≥ 20
- PowerShell 7 (để chạy script kiểm thử trên Windows)
- Tài khoản API AI (OpenRouter, AgentRouter hoặc mô hình nội bộ qua Ollama)

Xem thêm chi tiết trong `docs/ARCHITECTURE.md`.
