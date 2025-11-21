---
phase: testing
title: Chiến Lược Kiểm Tra - Backend Async Migration
description: Kiểm thử code async database
---

# Chiến Lược Kiểm Tra - Backend Async Migration

## Mục Tiêu Bao Phủ Kiểm Tra

**Chúng ta nhắm đến mức kiểm tra nào?**

- Đảm bảo 100% các service function đã chuyển đổi đều được test.
- Các test case cũ phải pass sau khi cập nhật sang async.

## Kiểm Tra Đơn Vị (Unit Test)

**Thành phần riêng lẻ nào cần kiểm tra?**

- Cần mock `AsyncSession`.
- Sử dụng `pytest.mark.asyncio` cho các test function.

Ví dụ:

```python
@pytest.mark.asyncio
async def test_create_user():
    # ... setup async session ...
    await create_user(session, data)
    # ... assert ...
```

## Kiểm Tra Tích Hợp

**Chúng ta kiểm tra tương tác thành phần như thế nào?**

- Sử dụng DB thật (test db) với `AsyncEngine`.
- Fixture `client` của FastAPI cần dùng `AsyncClient` (từ `httpx`) thay vì `TestClient` (sync) nếu muốn test full async flow, hoặc vẫn dùng `TestClient` nhưng app bên trong chạy async (FastAPI xử lý được). Tuy nhiên, tốt nhất là dùng `AsyncClient` để test đúng bản chất.

## Dữ Liệu Kiểm Tra

**Chúng ta sử dụng dữ liệu nào để kiểm tra?**

- Dữ liệu mẫu trong DB test.
- Cần reset DB sạch sẽ sau mỗi test case (dùng transaction rollback hoặc truncate).

## Báo Cáo & Bao Phủ Kiểm Tra

**Chúng ta xác minh và giao tiếp kết quả kiểm tra như thế nào?**

- Chạy `pytest` và đảm bảo xanh (pass).
