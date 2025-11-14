---
phase: design
title: Thiết Kế Hệ Thống & Kiến Trúc
description: Xác định kiến trúc kỹ thuật, các thành phần và mô hình dữ liệu
---

# Thiết Kế Hệ Thống & Kiến Trúc

## Tổng Quan Kiến Trúc

**Cấu trúc hệ thống cấp cao là gì?**

- Bao gồm sơ đồ mermaid nắm bắt các thành phần chính và mối quan hệ của chúng. Ví dụ:
  ```mermaid
  graph TD
    PublicLayout --> Navbar
    PublicLayout --> Footer
    PublicLayout --> AccountLayout
    AccountLayout --> SidebarMenu
    AccountLayout --> ContentArea
    ContentArea --> ProfilePage
    ContentArea --> AppointmentsPage
    ContentArea --> ServicesPage
    ContentArea --> NotificationsPage
  ```
- Các thành phần chính: PublicLayout (lớp ngoài), AccountLayout (2 cột), Page content (lớp trong).
- Lựa chọn stack: Next.js App Router, Shadcn/UI, TypeScript.

## Mô Hình Dữ Liệu

**Chúng ta cần quản lý dữ liệu nào?**

- User profile: Họ, Tên, Số điện thoại, Ngày sinh, Avatar.
- Appointments: Danh sách lịch hẹn với trạng thái.
- Services: Gói dịch vụ/liệu trình đã mua.
- Notifications: Danh sách thông báo từ Spa.

## Thiết Kế API

**Các thành phần giao tiếp như thế nào?**

- Sử dụng Supabase client để fetch user data.
- API calls qua apiRequests/ theo domain.
- Xác thực: Supabase JWT.

## Phân Tích Thành Phần

**Các khối xây dựng chính là gì?**

- Frontend: Layout components (Sidebar, ContentArea), Page components (Profile, etc.).
- Tích hợp: Supabase auth.

## Quyết Định Thiết Kế

**Tại sao chúng ta chọn cách tiếp cận này?**

- Nested layout để tái sử dụng public layout.
- 2 cột responsive với Shadcn/UI cho consistency.
- Client-side navigation để smooth UX.

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- Responsive trên mobile.
- Fast loading, no reload on menu click.
- Secure: Chỉ authenticated users.
