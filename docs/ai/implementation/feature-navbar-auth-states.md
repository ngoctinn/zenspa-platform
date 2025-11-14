---
phase: implementation
title: Hướng Dẫn Triển Khai
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
---

# Hướng Dẫn Triển Khai

## Thiết Lập Phát Triển

**Chúng ta bắt đầu như thế nào?**

- Cài đặt Shadcn/UI DropdownMenu nếu chưa có.
- Import Supabase client.

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

- Component trong `components/auth/`: AuthActions.tsx, NotificationIcon.tsx, UserProfileMenu.tsx.
- Navbar.tsx import và sử dụng chúng.

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

### Tính Năng Cốt Lõi

- AuthActions: Hiển thị nút Đăng nhập và Đăng ký khi chưa đăng nhập.
- NotificationIcon: Icon Bell với Badge.
- UserProfileMenu: Avatar với DropdownMenu.
- Navbar: Conditional render dựa trên user state từ Supabase, dùng "use client" vì hooks.

### Mẫu & Thực Tiễn Tốt Nhất

- Sử dụng Shadcn/UI components.
- Không hardcode text, dùng biến theme.

## Điểm Tích Hợp

**Các phần kết nối như thế nào?**

- Chi tiết tích hợp API
- Kết nối cơ sở dữ liệu
- Thiết lập dịch vụ bên thứ ba

## Xử Lý Lỗi

**Chúng ta xử lý thất bại như thế nào?**

- Chiến lược xử lý lỗi
- Cách tiếp cận ghi nhật ký
- Cơ chế thử lại/fallback

## Cân Nhắc Hiệu Suất

**Chúng ta giữ tốc độ như thế nào?**

- Chiến lược tối ưu hóa
- Cách tiếp cận cache
- Tối ưu hóa truy vấn
- Quản lý tài nguyên

## Ghi Chú Bảo Mật

**Các biện pháp bảo mật nào đang được áp dụng?**

- Xác thực/ủy quyền
- Xác thực đầu vào
- Mã hóa dữ liệu
- Quản lý bí mật
