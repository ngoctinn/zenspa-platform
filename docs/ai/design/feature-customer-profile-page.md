---
phase: design
title: Thiết Kế Hệ Thống & Kiến Trúc
description: Xác định kiến trúc kỹ thuật, các thành phần và mô hình dữ liệu
---

# Thiết Kế Hệ Thống & Kiến Trúc

## Tổng Quan Kiến Trúc

**Cấu trúc hệ thống cấp cao là gì?**

- Page: app/(auth)/account/profile/page.tsx
- Component: ProfileForm với avatar upload, inputs.
- API: Supabase client để fetch/update user data.

## Mô Hình Dữ Liệu

**Chúng ta cần quản lý dữ liệu nào?**

- User profile: firstName, lastName, phone, birthDate, avatarUrl.

## Thiết Kế API

**Các thành phần giao tiếp như thế nào?**

- Supabase auth.getUser() để lấy data.
- Supabase storage.upload() cho avatar.

## Phân Tích Thành Phần

**Các khối xây dựng chính là gì?**

- ProfileForm component với AvatarUpload, Input fields.
- Validation schema với zod.

## Quyết Định Thiết Kế

**Tại sao chúng ta chọn cách tiếp cận này?**

- Tái sử dụng Shadcn/UI cho form.
- Client-side update với optimistic UI.

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- Fast loading, secure (chỉ user của mình).
