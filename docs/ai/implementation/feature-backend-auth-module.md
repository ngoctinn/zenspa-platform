---
phase: implementation
title: Hướng Dẫn Triển Khai
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
feature: backend-auth-module
---

# Hướng Dẫn Triển Khai

## Thiết Lập Phát Triển

**Chúng ta bắt đầu như thế nào?**

- Prerequisites: Python 3.12, Supabase account.
- Setup: pip install -r requirements.txt, set env vars.

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

- app/core/auth.py: Auth logic.
- app/api/admin.py: Admin routes.

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

### Tính Năng Cốt Lõi

- JWT Verify: Sử dụng PyJWK, decode RS256.
- Role Check: Extract từ payload.

### Mẫu & Thực Tiễn Tốt Nhất

- Dependency injection: get_current_user.
- Error handling: HTTPException.

## Điểm Tích Hợp

**Các phần kết nối như thế nào?**

- Supabase: JWKS fetch, metadata update.

## Xử Lý Lỗi

**Chúng ta xử lý thất bại như thế nào?**

- JWT invalid: 401.
- Network error: 500.

## Cân Nhắc Hiệu Suất

**Chúng ta giữ tốc độ như thế nào?**

- Cache JWKS if needed.

## Ghi Chú Bảo Mật

**Các biện pháp bảo mật nào đang được áp dụng?**

- Verify JWT, role checks, no key exposure.
