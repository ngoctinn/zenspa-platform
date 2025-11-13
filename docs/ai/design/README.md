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
    Client -->|HTTPS| API
    API --> ServiceA
    API --> ServiceB
    ServiceA --> Database[(DB)]
  ```
- Các thành phần chính và trách nhiệm của chúng
- Lựa chọn stack công nghệ và lý do

## Mô Hình Dữ Liệu

**Chúng ta cần quản lý dữ liệu nào?**

- Các thực thể cốt lõi và mối quan hệ của chúng
- Schema/cấu trúc dữ liệu
- Luồng dữ liệu giữa các thành phần

## Thiết Kế API

**Các thành phần giao tiếp như thế nào?**

- API bên ngoài (nếu áp dụng)
- Giao diện nội bộ
- Định dạng yêu cầu/phản hồi
- Cách tiếp cận xác thực/ủy quyền

## Phân Tích Thành Phần

**Các khối xây dựng chính là gì?**

- Các thành phần frontend (nếu áp dụng)
- Các dịch vụ/mô-đun backend
- Lớp cơ sở dữ liệu/lưu trữ
- Tích hợp bên thứ ba

## Quyết Định Thiết Kế

**Tại sao chúng ta chọn cách tiếp cận này?**

- Các quyết định kiến trúc chính và sự đánh đổi
- Các lựa chọn thay thế được xem xét
- Các mẫu và nguyên tắc được áp dụng

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- Mục tiêu hiệu suất
- Cân nhắc khả năng mở rộng
- Yêu cầu bảo mật
- Nhu cầu độ tin cậy/khả dụng
