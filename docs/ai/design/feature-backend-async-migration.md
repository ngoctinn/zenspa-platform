---
phase: design
title: Thiết Kế Hệ Thống & Kiến Trúc - Backend Async Migration
description: Thiết kế chuyển đổi sang AsyncSession và AsyncEngine
---

# Thiết Kế Hệ Thống & Kiến Trúc - Backend Async Migration

## Tổng Quan Kiến Trúc

**Cấu trúc hệ thống cấp cao là gì?**

- Hệ thống vẫn giữ kiến trúc Modular Monolith với FastAPI.
- Thay đổi chính nằm ở tầng **Infrastructure (Database)**:
  - Chuyển từ `create_engine` (sync) sang `create_async_engine` (async).
  - Chuyển từ `Session` (sync) sang `AsyncSession` (async).
- Driver kết nối DB: `psycopg2` (hoặc default) -> `asyncpg`.

## Mô Hình Dữ Liệu

**Chúng ta cần quản lý dữ liệu nào?**

- Không thay đổi về Schema (cấu trúc bảng).
- Thay đổi về cách truy xuất:
  - `session.query(...)` -> `await session.exec(select(...))` (SQLModel ưu tiên `exec` + `select`).
  - `session.commit()` -> `await session.commit()`.
  - `session.refresh()` -> `await session.refresh()`.
  - Lazy loading (truy cập thuộc tính quan hệ) không hoạt động mặc định trong async. Cần dùng `select(...).options(selectinload(...))` hoặc load trước dữ liệu cần thiết.

## Thiết Kế API

**Các thành phần giao tiếp như thế nào?**

- API Endpoint Signature sẽ thay đổi:
  - `def endpoint(session: Session = Depends(get_session))`
  - -> `async def endpoint(session: AsyncSession = Depends(get_async_session))`
- Các hàm trong Service/Controller cũng phải chuyển thành `async def`.

## Phân Tích Thành Phần

**Các khối xây dựng chính là gì?**

1.  **`app/core/database.py`**:

    - Khởi tạo `AsyncEngine`.
    - Tạo `async_sessionmaker`.
    - Hàm `get_async_session` yield `AsyncSession`.

2.  **Services (`app/modules/*/services.py`)**:

    - Chuyển đổi logic sang async.
    - Thay thế các query style cũ (`session.query`) sang style mới (`session.exec(select)`).

3.  **Dependencies**:
    - Cập nhật `get_session` dependency injection.

## Quyết Định Thiết Kế

**Tại sao chúng ta chọn cách tiếp cận này?**

- **Sử dụng `sqlmodel.ext.asyncio.session.AsyncSession`**: Đây là chuẩn hỗ trợ của SQLModel cho async.
- **Sử dụng `asyncpg`**: Driver nhanh nhất và ổn định nhất cho PostgreSQL async với Python.
- **Eager Loading**: Vì async không hỗ trợ lazy loading ngầm định (implicit lazy loading) tốt như sync, chúng ta sẽ ưu tiên explicit loading (dùng `selectinload` hoặc join) để tránh lỗi `DetachedInstanceError` hoặc `MissingGreenlet`.

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- **Hiệu năng**: Tăng throughput (số request/giây) nhờ non-blocking I/O.
- **Độ tin cậy**: Đảm bảo connection pool được quản lý tốt, tránh leak connection.
