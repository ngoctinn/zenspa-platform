---
phase: design
title: Thiết Kế Hệ Thống & Kiến Trúc
description: Xác định kiến trúc kỹ thuật, các thành phần và mô hình dữ liệu
---

# Thiết Kế Hệ Thống & Kiến Trúc

## Tổng Quan Kiến Trúc

**Cấu trúc hệ thống cấp cao là gì?**

- Frontend: Next.js với component Navbar chứa logic trạng thái đăng nhập.
- Component tách riêng: NotificationIcon, UserProfileMenu, AuthActions.
- Sử dụng Supabase auth để xác định trạng thái user.
  ```mermaid
  graph TD
    Navbar --> AuthActions[AuthActions: CTA cho chưa đăng nhập]
    Navbar --> NotificationIcon[NotificationIcon: Icon với badge]
    Navbar --> UserProfileMenu[UserProfileMenu: Dropdown menu]
    UserProfileMenu --> DropdownMenu[DropdownMenu từ Shadcn/UI]
  ```
- Các thành phần chính: Navbar (container), AuthActions, NotificationIcon, UserProfileMenu.
- Lựa chọn stack: Next.js, TypeScript, Shadcn/UI để đảm bảo nhất quán.

## Mô Hình Dữ Liệu

**Chúng ta cần quản lý dữ liệu nào?**

- User data: name, avatar (từ Supabase auth).
- Notification count: số lượng thông báo chưa đọc (giả định từ API hoặc state local).
- Schema: User { id, name, avatar }, Notification { count }.

## Thiết Kế API

**Các thành phần giao tiếp như thế nào?**

- Sử dụng Supabase auth để lấy user session.
- API nội bộ: Hàm getUser() từ Supabase client.
- Định dạng: JSON cho user data.

## Phân Tích Thành Phần

**Các khối xây dựng chính là gì?**

- AuthActions: Component cho CTA (Đăng nhập, Đăng ký).
- NotificationIcon: Icon chuông với badge số lượng.
- UserProfileMenu: Avatar/tên với dropdown (Hồ sơ, Lịch hẹn, Đăng xuất).
- Tích hợp: Shadcn/UI DropdownMenu.

## Quyết Định Thiết Kế

**Tại sao chúng ta chọn cách tiếp cận này?**

- Tách component để tái sử dụng, tránh code lặp.
- Sử dụng Shadcn/UI cho nhất quán design.
- Không dùng global state, chỉ state local trong Navbar.

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- Hiệu suất: Load nhanh, không lag.
- Bảo mật: Sử dụng Supabase auth an toàn.
