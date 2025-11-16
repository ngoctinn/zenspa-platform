---
phase: design
title: Thiết Kế Hệ Thống & Kiến Trúc
description: Xác định kiến trúc kỹ thuật, các thành phần và mô hình dữ liệu
---

# Thiết Kế Hệ Thống & Kiến Trúc

## Tổng Quan Kiến Trúc

**Cấu trúc hệ thống cấp cao là gì?**

- Bao gồm sơ đồ mermaid nắm bắt các thành phần chính và mối quan hệ của chúng.
  ```mermaid
  graph TD
    User -->|Signup| SupabaseAuth[Supabase Auth]
    SupabaseAuth -->|Trigger Hook| PostgresFunction[Postgres Function]
    PostgresFunction -->|Insert| ProfilesTable[(profiles table)]
    User -->|Login| Frontend[Next.js Frontend]
    Frontend -->|GET/PUT /me| Backend[FastAPI Backend]
    Backend -->|Query/Update| ProfilesTable
    Frontend -->|Upload Avatar| SupabaseStorage[Supabase Storage]
  ```
- Các thành phần: Supabase Auth (xác thực), Postgres Function (auto create), Backend API (CRUD), Frontend UI (form), Supabase Storage (avatar).
- Lựa chọn stack: Supabase cho DB/Auth, FastAPI cho API, Next.js cho UI – tuân thủ project stack.

## Mô Hình Dữ Liệu

**Chúng ta cần quản lý dữ liệu nào?**

- Thực thể: Profile (SQLModel, one-to-one với auth.users).
- Schema: id (UUID), email, full_name, phone, birth_date, avatar_url, role, created_at, updated_at.
- Luồng dữ liệu: Define model → Alembic migration → Apply to Supabase DB → Hook insert → API query/update.

## Thiết Kế API

**Các thành phần giao tiếp như thế nào?**

- API nội bộ: GET /api/v1/users/me (fetch profile), PUT /api/v1/users/me (update profile).
- Định dạng: JSON request/response, Pydantic validation.
- Xác thực: Bearer JWT từ Supabase.

## Phân Tích Thành Phần

**Các khối xây dựng chính là gì?**

- Frontend: ProfileForm component (form update), UserProfileMenu (display).
- Backend: Module customer (models, schemas, service, routes).
- DB: Bảng profiles với RLS.
- Storage: Supabase Storage cho avatar.

## Quyết Định Thiết Kế

**Tại sao chúng ta chọn cách tiếp cận này?**

- Sử dụng Supabase DB thay vì DB riêng: Đơn giản, tích hợp sẵn với Auth.
- Auth Hook: Sync ngay, tránh lazy creation delay.
- Module customer: Tuân thủ kiến trúc modular.
- Thay thế: Metadata only (ít mở rộng), DB riêng (phức tạp hơn).

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- Hiệu suất: API < 500ms.
- Bảo mật: RLS, JWT verify.
- Khả dụng: 99.9%, error handling tốt.
