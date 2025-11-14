---
phase: implementation
title: Hướng Dẫn Triển Khai
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
---

# Hướng Dẫn Triển Khai

## Thiết Lập Phát Triển

**Chúng ta bắt đầu như thế nào?**

- Đảm bảo Next.js, Shadcn/UI đã cài.
- Chạy pnpm install nếu cần.

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

- app/(auth)/account/layout.tsx: AccountLayout
- components/auth/AccountSidebar.tsx: Sidebar component
- components/auth/AccountContent.tsx: Content wrapper

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

### Tính Năng Cốt Lõi

- Layout: Sử dụng flexbox cho 2 cột.
- Sidebar: List các menu items với Link from next/link.
- Responsive: Sử dụng hidden/lg:flex cho mobile.

### Mẫu & Thực Tiễn Tốt Nhất

- Shadcn/UI: Button, Card, etc.
- TypeScript: Strict typing.

## Điểm Tích Hợp

**Các phần kết nối như thế nào?**

- Nested trong public layout.
- Supabase auth check.

## Xử Lý Lỗi

**Chúng ta xử lý thất bại như thế nào?**

- Redirect nếu không auth.

## Cân Nhắc Hiệu Suất

**Chúng ta giữ tốc độ như thế nào?**

- Lazy load components nếu cần.

## Ghi Chú Bảo Mật

**Các biện pháp bảo mật nào đang được áp dụng?**

- Auth guard.
