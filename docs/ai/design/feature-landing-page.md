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
    Client[Khách hàng] -->|HTTPS| LandingPage[Landing Page Next.js]
  ```
- Các thành phần chính: Frontend (Next.js với Shadcn/UI).
- Lựa chọn stack: Next.js cho SEO và performance, Shadcn/UI cho UI nhất quán.

## Mô Hình Dữ Liệu

**Chúng ta cần quản lý dữ liệu nào?**

- Không cần mô hình dữ liệu động; chỉ hiển thị nội dung tĩnh (dịch vụ, testimonials).

## Thiết Kế API

**Các thành phần giao tiếp như thế nào?**

- Không có API trong giai đoạn này.

## Phân Tích Thành Phần

**Các khối xây dựng chính là gì?**

- Frontend: HeroSection, ServicesBlock, Testimonials, Footer.

## Quyết Định Thiết Kế

**Tại sao chúng ta chọn cách tiếp cận này?**

- Mobile-first: Vì người dùng chủ yếu dùng mobile.
- MVP đơn giản: Tập trung vào conversion, tránh phức tạp.
- Shadcn/UI: Tuân thủ quy tắc dự án, dễ tùy chỉnh.

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- Hiệu suất: Tải nhanh (<3s).
- Bảo mật: Xác thực input cơ bản.
- Khả năng mở rộng: Dễ thêm blocks sau.
