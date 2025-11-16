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
    Admin[Admin User] -->|JWT| Frontend[Next.js Frontend]
    Frontend -->|API Call| Backend[FastAPI Backend]
    Backend -->|Check User| Supabase[Supabase Auth]
    Backend -->|Invite New| Supabase
    Backend -->|Update Roles| Database[(PostgreSQL)]
    Supabase -->|Send Email| User[Staff User]
    User -->|Accept Invite| Frontend
    Database -->|User Roles| Backend
  ```
- Các thành phần chính: Frontend (Next.js) cho giao diện Admin, Backend (FastAPI) xử lý logic mời/gán, Supabase quản lý Auth và gửi email, PostgreSQL lưu vai trò.
- Lựa chọn stack: Tuân thủ quy tắc dự án (FastAPI, Supabase, Next.js).

## Mô Hình Dữ Liệu

**Chúng ta cần quản lý dữ liệu nào?**

- Thực thể: User (liên kết với auth.users), Role (enum: customer, technician, receptionist, admin), UserRoleLink (bảng liên kết user_id và role_name).
- Schema: UserRoleLink với user_id (UUID), role_name (string), created_at, updated_at.
- Luồng dữ liệu: Admin gửi request → Backend kiểm tra user → Cập nhật DB hoặc gọi Supabase invite → Gửi email.

## Thiết Kế API

**Các thành phần giao tiếp như thế nào?**

- API nội bộ: POST /api/v1/admin/invite-staff với body {email, role}.
- Phản hồi: Thành công hoặc lỗi (user exists, role already assigned, etc.).
- Xác thực: JWT của Admin, kiểm tra role 'admin'.

## Phân Tích Thành Phần

**Các khối xây dựng chính là gì?**

- Frontend: Component InviteStaffForm, API request inviteStaff.
- Backend: Module admin với schemas, service, routes.
- Database: Bảng UserRoleLink, trigger cho việc gán vai trò sau invite.

## Quyết Định Thiết Kế

**Tại sao chúng ta chọn cách tiếp cận này?**

- Sử dụng Supabase invite để tận dụng built-in email sending.
- Bảng liên kết cho vai trò nhiều-nhiều thay vì cột trong User để linh hoạt.
- Xử lý logic ở backend để đảm bảo bảo mật và nhất quán.

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- Hiệu suất: Response time < 2s cho API invite.
- Bảo mật: Chỉ Admin có quyền, validate input email và role.
- Độ tin cậy: Xử lý lỗi khi Supabase unavailable, rollback nếu cần.
