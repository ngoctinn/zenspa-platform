---
phase: implementation
title: Hướng Dẫn Triển Khai
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
---

# Hướng Dẫn Triển Khai

## Thiết Lập Phát Triển

**Chúng ta bắt đầu như thế nào?**

- Điều kiện tiên quyết: Supabase project với service_role key, PostgreSQL DB.
- Các bước: Cài đặt dependencies, chạy migration, start backend và frontend.

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

- Backend: app/modules/admin/ với admin_schemas.py, admin_service.py, admin_routes.py
- Frontend: components/admin/InviteStaffForm.tsx, apiRequests/admin.ts

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

### Tính Năng Cốt Lõi

- Xử lý invite: Kiểm tra user tồn tại, gọi supabase.auth.admin.inviteUserByEmail với metadata.
- Gán role: Thêm record vào UserRoleLink, gửi email thông báo.

### Mẫu & Thực Tiễn Tốt Nhất

- Sử dụng SQLModel cho models, Pydantic cho schemas.
- Validate input với Field validators.

## Điểm Tích Hợp

**Các phần kết nối như thế nào?**

- Backend gọi Supabase client với service_role.
- Frontend gửi JWT trong header.

## Xử Lý Lỗi

**Chúng ta xử lý thất bại như thế nào?**

- Catch exceptions từ Supabase, return appropriate error messages.

## Cân Nhắc Hiệu Suất

**Chúng ta giữ tốc độ như thế nào?**

- Cache user checks nếu cần, nhưng API đơn giản nên OK.

## Ghi Chú Bảo Mật

**Các biện pháp bảo mật nào đang được áp dụng?**

- Chỉ Admin role có thể access endpoint.
- Validate email format, role enum.
