---
phase: design
title: Thiết Kế Hệ Thống & Kiến Trúc
description: Xác định kiến trúc kỹ thuật, các thành phần và mô hình dữ liệu
feature: backend-user-profile-api
---

# Thiết Kế Hệ Thống & Kiến Trúc

## Tổng Quan Kiến Trúc

**Cấu trúc hệ thống cấp cao là gì?**

- Bao gồm sơ đồ mermaid nắm bắt các thành phần chính và mối quan hệ của chúng.
  ```mermaid
  graph TD
    Frontend -->|JWT| Backend
    Backend -->|Verify| Supabase[(Supabase Auth)]
    Backend -->|Return| UserInfo[User Profile Info]
  ```
- Các thành phần chính: Frontend (client), Backend (FastAPI), Supabase (auth provider).
- Lựa chọn stack: FastAPI, PyJWT, get_current_user dependency.

## Mô Hình Dữ Liệu

**Chúng ta cần quản lý dữ liệu nào?**

- Thực thể: User info từ JWT (id, email, role).
- Schema: JSON response với fields từ payload.
- Luồng: Extract từ JWT, không query DB.

## Thiết Kế API

**Các thành phần giao tiếp như thế nào?**

- API nội bộ: GET /api/v1/users/me (authenticated).
- Giao diện: FastAPI endpoint, return JSON.
- Định dạng: Bearer token, JSON response.
- Xác thực: JWT verify via get_current_user.

## Phân Tích Thành Phần

**Các khối xây dựng chính là gì?**

- app/api/users.py: Endpoint cho user profile.
- app/core/auth.py: get_current_user dependency (đã có).

## Quyết Định Thiết Kế

**Tại sao chúng ta chọn cách tiếp cận này?**

- Sử dụng existing auth module để consistency.
- Alternatives: Query DB (phức tạp hơn), custom endpoint (duplicate code).

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- Performance: <100ms.
- Security: JWT verify, no expose sensitive data.
- Reliability: Handle JWT errors.
