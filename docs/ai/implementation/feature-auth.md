---
phase: implementation
title: Hướng Dẫn Triển Khai - feature-auth
description: Hướng dẫn triển khai kỹ thuật cho giao diện xác thực
---

# Hướng Dẫn Triển Khai

## Thiết Lập Phát Triển

- Vào thư mục frontend: `cd frontend`
- Cài phụ thuộc nếu cần: `pnpm install` (project đã có `package.json`)
- Khởi động dev: `pnpm dev`

## Cấu Trúc Mã (đề xuất)

```
frontend/components/auth/
  - SignInForm.tsx
  - SignUpForm.tsx
  - ResetPasswordForm.tsx
  - messages.ts
```

## Ghi Chú Triển Khai

### Tính Năng Cốt Lõi

- `SignUpForm`: sử dụng `react-hook-form` (`mode: 'onChange'`), rules: email pattern, password length 8–20 + chữ + số, confirm must match.
- `SignInForm`: email pattern + password required.
- `ResetPasswordForm`: email pattern.

### Mẫu & Thực Tiễn Tốt Nhất

- Không hardcode chuỗi hiển thị; dùng `messages.ts`.
- Sử dụng `Form`, `FormField`, `FormItem`, `FormLabel`, `FormControl`, `FormMessage` để tận dụng `aria-*` và styling sẵn có.

## Điểm Tích Hợp

- Mock API: đặt ở `frontend/app/api/auth/*` (nếu muốn). Nội dung hiện tại sẽ gọi `fetch('/api/auth/register', { method: 'POST' ... })` → mock bằng `setTimeout`.

## Xử Lý Lỗi

- Hiển thị lỗi client ngay inline.
- Khi gọi API, nếu lỗi server, show toast/dialog với message server.

## Cân Nhắc Hiệu Suất

- Validation chạy client; không có tác vụ nặng.

## Ghi Chú Bảo Mật

- Không lưu mật khẩu ở localStorage, sessionStorage.
- Gọi API qua HTTPS (ở production).
