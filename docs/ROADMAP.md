# Lộ trình dự án tra cứu HS code

Tài liệu này ghi nhận trạng thái hiện tại của các hạng mục trong hệ thống, giúp theo dõi tiến độ và xác định các bước tiếp theo.

## Đã hoàn thành ✅
- Thiết lập kiến trúc tổng thể với FastAPI (backend), PostgreSQL, Next.js (frontend) và tài liệu kiến trúc chi tiết.
- Cấu hình hạ tầng cơ bản: Docker Compose, Dockerfile cho backend/frontend, workflow CI GitHub Actions và script PowerShell chạy lint/kiểm thử.
- Backend FastAPI: mô hình dữ liệu, repository tìm kiếm, endpoint `GET /documents`, `GET /documents/{id}`, `GET /health`, hỗ trợ truy vấn tiếng Việt và phân trang.
- Frontend Next.js tiếng Việt: form tra cứu, bảng kết quả, phân trang, liên kết tải PDF gốc và cấu hình Tailwind.

## Đang thực hiện 🚧
- Hoàn thiện bộ crawler (CustomsClient, DownloadManager, Scheduler) để đồng bộ danh sách văn bản và tải PDF về hệ thống lưu trữ.
- Hoàn thiện pipeline xử lý PDF & AI (PDFExtractor, AIRouter, PostProcessor) để bóc tách nội dung, chuẩn hóa dữ liệu và ghi vào cơ sở dữ liệu.
- Kết nối endpoint đồng bộ `/api/v1/sync/run` với crawler và pipeline để kích hoạt quy trình cập nhật dữ liệu tự động.

## Sẽ thực hiện ⏳
- Tích hợp đầy đủ pipeline AI/OCR vào quy trình đồng bộ, bổ sung kiểm soát chất lượng dữ liệu và cơ chế retry.
- Mở rộng API (lọc nâng cao, thống kê, phân quyền) và frontend (xuất báo cáo, quản trị nội dung, bộ lọc chi tiết theo thời gian, lĩnh vực).
- Thiết lập giám sát, logging nâng cao, cache kết quả tra cứu và tối ưu hiệu năng cho môi trường triển khai thực tế.
- Nghiên cứu bổ sung chú giải HS 2022, liên kết với nguồn dữ liệu khác và cải tiến trải nghiệm người dùng (tìm kiếm gợi ý, từ khóa liên quan).

Tài liệu sẽ được cập nhật sau mỗi giai đoạn để phản ánh trạng thái mới nhất.
