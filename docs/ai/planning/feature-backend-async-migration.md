---
phase: planning
title: Lập Kế Hoạch Dự Án - Backend Async Migration
description: Kế hoạch chuyển đổi sang Async Database
---

# Lập Kế Hoạch Dự Án & Phân Tích Nhiệm Vụ - Backend Async Migration

## Mốc Quan Trọng

**Các điểm kiểm tra chính là gì?**

- [ ] Mốc 1: Cấu hình Core Database Async thành công.
- [ ] Mốc 2: Chuyển đổi xong Module User (Foundation).
- [ ] Mốc 3: Chuyển đổi xong các Module còn lại và Tests.

## Phân Tích Nhiệm Vụ

**Công việc cụ thể nào cần thực hiện?**

### Giai Đoạn 1: Nền Tảng (Core)

- [ ] Nhiệm vụ 1.1: Cài đặt driver `asyncpg` và cập nhật `requirements.txt`.
- [ ] Nhiệm vụ 1.2: Cập nhật `app/core/database.py` để dùng `AsyncEngine` và `AsyncSession`.
- [ ] Nhiệm vụ 1.3: Cập nhật `alembic/env.py` để hỗ trợ migration với async engine (nếu cần thiết, hoặc giữ sync cho migration offline).

### Giai Đoạn 2: Chuyển Đổi Module User (Foundation)

- [ ] Nhiệm vụ 2.1: Refactor `app/modules/user/user_service.py` sang async.
- [ ] Nhiệm vụ 2.2: Refactor `app/modules/user/user_routes.py` (API) sang async và dùng `get_async_session`.
- [ ] Nhiệm vụ 2.3: Kiểm tra và sửa các lỗi liên quan đến lazy loading trong User module.

### Giai Đoạn 3: Chuyển Đổi Các Module Khác & Cleanup

- [ ] Nhiệm vụ 3.1: Refactor các module khác (nếu có code mẫu).
- [ ] Nhiệm vụ 3.2: Xóa bỏ các cấu hình sync cũ không còn dùng.

### Giai Đoạn 4: Testing

- [ ] Nhiệm vụ 4.1: Cập nhật cấu hình `conftest.py` để hỗ trợ `pytest-asyncio` và `AsyncSession`.
- [ ] Nhiệm vụ 4.2: Fix các unit test bị fail do chuyển sang async.

## Phụ Thuộc

**Điều gì cần xảy ra theo thứ tự nào?**

- Giai đoạn 1 phải xong trước Giai đoạn 2.
- Module User là nền tảng, nên làm trước các module nghiệp vụ khác.

## Thời Gian & Ước Tính

**Khi nào mọi thứ sẽ hoàn thành?**

- Giai đoạn 1: 1 giờ.
- Giai đoạn 2: 2 giờ.
- Giai đoạn 3 & 4: 2 giờ.
- Tổng cộng: ~5 giờ làm việc.

## Rủi Ro & Giảm Thiểu

**Điều gì có thể sai sót?**

- **Rủi ro:** Lazy loading gây lỗi runtime.
  - **Giảm thiểu:** Review kỹ các query có quan hệ (relationship), viết test case cover các trường hợp này.
- **Rủi ro:** Alembic migration gặp vấn đề.
  - **Giảm thiểu:** Test kỹ lệnh `alembic upgrade head` sau khi đổi config.

## Tài Nguyên Cần Thiết

**Chúng ta cần gì để thành công?**

- Thư viện: `asyncpg`, `pytest-asyncio`.
