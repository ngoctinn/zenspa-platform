---
phase: design
title: Thiết Kế Hệ Thống & Kiến Trúc
description: Xác định kiến trúc kỹ thuật, các thành phần và mô hình dữ liệu
feature: backend-auth-module
---

# Thiết Kế Hệ Thống & Kiến Trúc

## Tổng Quan Kiến Trúc

**Cấu trúc hệ thống cấp cao là gì?**

- Bao gồm sơ đồ mermaid nắm bắt các thành phần chính và mối quan hệ của chúng.
  ```mermaid
  graph TD
    Frontend -->|JWT| Backend
    Backend -->|Verify| Supabase[(Supabase Auth)]
    Backend -->|Enforce| API[Protected APIs]
    Admin -->|API Call| Backend
    Backend -->|Update| Supabase
  ```
- Các thành phần chính: Frontend (client), Backend (FastAPI), Supabase (auth provider).
- Lựa chọn stack: PyJWT (verify), supabase-py (admin), FastAPI dependencies.

## Mô Hình Dữ Liệu

**Chúng ta cần quản lý dữ liệu nào?**

- Thực thể: User (supabase_user_id, role), JWT payload (sub, role, exp).
- Schema: Role enum (customer, receptionist, technician, admin).
- Luồng: JWT chứa role từ Supabase metadata, backend extract không query DB.

## Thiết Kế API

**Các thành phần giao tiếp như thế nào?**

- API nội bộ: /api/v1/admin/users/{id}/role (PUT, admin only).
- Giao diện: FastAPI dependency get_current_user trả dict user info.
- Định dạng: JSON, Bearer token.
- Xác thực: JWT verify, role check.

## Phân Tích Thành Phần

**Các khối xây dựng chính là gì?**

- app/core/auth.py: Verify JWT, get_current_user.
- app/api/admin.py: Admin endpoints.
- Supabase: Metadata storage.

## Quyết Định Thiết Kế

**Tại sao chúng ta chọn cách tiếp cận này?**

- JWT verify thay DB query: Nhanh, stateless.
- Supabase metadata: Đơn giản, không cần DB sync ban đầu.
- Alternatives: DB roles (phức tạp hơn), custom auth (vi phạm quy tắc).

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- Performance: <100ms verify.
- Security: Không expose keys, rate limit.
- Reliability: Handle JWKS errors.
