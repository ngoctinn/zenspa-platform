---
phase: implementation
title: Hướng Dẫn Triển Khai
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
---

# Hướng Dẫn Triển Khai

## Thiết Lập Phát Triển

**Chúng ta bắt đầu như thế nào?**

- Điều kiện: Supabase account, backend config với DB URL.
- Bước: Define SQLModel, chạy alembic revision --autogenerate, alembic upgrade head, setup hook.

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

- Backend: app/modules/customer/ (models.py, etc.).
- Frontend: components/auth/ProfileForm.tsx.

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

### Tính Năng Cốt Lõi

- Migration: Sử dụng Alembic để tạo bảng từ SQLModel.
- Auto create: Hook insert profile.
- CRUD: API GET/PUT với validation.

### Mẫu & Thực Tiễn

- SQLModel cho models, Pydantic schemas.
- RLS policies.

## Điểm Tích Hợp

**Các phần kết nối như thế nào?**

- Backend query Supabase DB.
- Frontend call backend API.

## Xử Lý Lỗi

**Chúng ta xử lý thất bại như thế nào?**

- Try-catch, return error JSON.

## Bảo Mật

**Các biện pháp bảo mật nào đang được áp dụng?**

- RLS, JWT verify.
