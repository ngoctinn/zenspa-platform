---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề - Backend Async Migration
description: Chuyển đổi các thao tác cơ sở dữ liệu sang bất đồng bộ (Async) để cải thiện hiệu năng
---

# Yêu Cầu & Hiểu Vấn Đề - Backend Async Migration

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

- Hiện tại, backend FastAPI đang sử dụng `Session` đồng bộ (sync) của SQLModel.
- Các thao tác I/O với cơ sở dữ liệu (query, commit) là blocking, làm chặn event loop của FastAPI.
- Điều này làm giảm khả năng xử lý đồng thời (concurrency) của ứng dụng, đặc biệt khi có nhiều request hoặc tải cao.
- Developer cần viết code async chuẩn để tận dụng tối đa sức mạnh của FastAPI.

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

- **Mục tiêu chính:** Chuyển đổi toàn bộ lớp truy cập dữ liệu (Data Access Layer) sang sử dụng `AsyncSession` và `AsyncEngine`.
- **Mục tiêu phụ:** Refactor code base để tuân thủ chuẩn async/await của Python hiện đại.
- **Không mục tiêu:** Thay đổi cấu trúc bảng (schema) hoặc logic nghiệp vụ (business logic). Chỉ thay đổi cách gọi DB.

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

- **Là một Developer**, tôi muốn sử dụng `AsyncSession` để viết code không chặn (non-blocking), giúp ứng dụng phản hồi nhanh hơn.
- **Là một System Admin**, tôi muốn hệ thống chịu tải tốt hơn mà không cần tăng quá nhiều tài nguyên phần cứng.

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

- File `core/database.py` cấu hình `AsyncEngine` và `get_async_session` thành công.
- Tất cả các service (User, Auth, v.v.) sử dụng `AsyncSession` và từ khóa `await` cho các thao tác DB.
- Dependency `get_session` trong các API route được thay thế bằng `get_async_session`.
- Toàn bộ Unit Test và Integration Test chạy qua (pass) mà không có lỗi liên quan đến event loop hoặc DB connection.
- Không còn code sử dụng `Session` (sync) trong các luồng xử lý request chính.

## Ràng Buộc & Giả Định

**Chúng ta cần làm việc trong giới hạn nào?**

- **Ràng buộc kỹ thuật:** Phải sử dụng driver `asyncpg` cho PostgreSQL.
- **Ràng buộc kỹ thuật:** `AsyncSession` phải được import từ `sqlmodel.ext.asyncio.session` (hoặc tương đương hỗ trợ bởi SQLModel).
- **Giả định:** Thư viện `sqlmodel` và `alembic` hỗ trợ tốt việc chuyển đổi này (Alembic có thể vẫn chạy sync hoặc cần cấu hình lại `env.py` để hỗ trợ async nếu cần, nhưng thường migration chạy offline/sync cũng ổn, tuy nhiên tốt nhất là cấu hình async cho đồng bộ).

## Câu Hỏi & Vấn Đề Mở

**Chúng ta vẫn cần làm rõ gì?**

- Cần kiểm tra xem `alembic/env.py` có cần cập nhật để hỗ trợ `async_engine` không? (Thường là có để dùng `run_sync`).
- Các thư viện bên thứ 3 khác có đang dùng sync session không?
