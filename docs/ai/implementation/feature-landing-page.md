---
phase: implementation
title: Hướng Dẫn Triển Khai
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
---

# Hướng Dẫn Triển Khai

## Thiết Lập Phát Triển

**Chúng ta bắt đầu như thế nào?**

- pnpm install, setup Supabase client.

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

- app/(public)/page.tsx: Landing page.
- components/: Blocks như HeroSection, BookingForm.

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

### Tính Năng Cốt Lõi

- Hero: Sử dụng shadcn Button cho CTA (liên kết đến liên hệ).
- Blocks: Hiển thị nội dung tĩnh từ props hoặc config.

### Mẫu & Thực Tiễn Tốt Nhất

- Mobile-first với Tailwind.
- Không hardcode màu sắc.

## Điểm Tích Hợp

**Các phần kết nối như thế nào?**

- Không có tích hợp backend trong giai đoạn này.

## Xử Lý Lỗi

**Chúng ta xử lý thất bại như thế nào?**

- Không áp dụng.

## Cân Nhắc Hiệu Suất

**Chúng ta giữ tốc độ như thế nào?**

- Optimize images.

## Ghi Chú Bảo Mật

**Các biện pháp bảo mật nào đang được áp dụng?**

- Không áp dụng.
