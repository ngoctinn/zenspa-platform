---
phase: implementation
title: Hướng Dẫn Triển Khai
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
---

# Hướng Dẫn Triển Khai

## Thiết Lập Phát Triển

**Chúng ta bắt đầu như thế nào?**

- Đảm bảo Shadcn/UI có Button, Input, Form, Avatar.

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

- app/(auth)/account/profile/page.tsx
- components/auth/ProfileForm.tsx

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

- Sử dụng react-hook-form với zodResolver.
- Avatar upload với Supabase storage.

## Điểm Tích Hợp

**Các phần kết nối như thế nào?**

- Fetch user data từ Supabase.
- Update qua API.

## Xử Lý Lỗi

**Chúng ta xử lý thất bại như thế nào?**

- Toast cho errors.

## Cân Nhắc Hiệu Suất

**Chúng ta giữ tốc độ như thế nào?**

- Lazy load avatar.

## Ghi Chú Bảo Mật

**Các biện pháp bảo mật nào đang được áp dụng?**

- Chỉ user của mình update.
