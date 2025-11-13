---
phase: deployment
title: Chiến Lược Triển Khai
description: Xác định quy trình triển khai, hạ tầng và thủ tục phát hành
---

# Chiến Lược Triển Khai

## Hạ Tầng

**Ứng dụng sẽ chạy ở đâu?**

- Nền tảng lưu trữ (AWS, GCP, Azure, v.v.)
- Các thành phần hạ tầng (máy chủ, cơ sở dữ liệu, v.v.)
- Phân tách môi trường (dev, staging, production)

## Pipeline Triển Khai

**Chúng ta triển khai thay đổi như thế nào?**

### Quy Trình Xây Dựng

- Các bước xây dựng và lệnh
- Biên dịch/tối ưu hóa tài sản
- Cấu hình môi trường

### Pipeline CI/CD

- Cổng kiểm tra tự động
- Tự động hóa xây dựng
- Tự động hóa triển khai

## Cấu Hình Môi Trường

**Cài đặt nào khác nhau theo môi trường?**

### Phát Triển

- Chi tiết cấu hình
- Thiết lập cục bộ

### Staging

- Chi tiết cấu hình
- Môi trường kiểm tra

### Sản Xuất

- Chi tiết cấu hình
- Thiết lập giám sát

## Các Bước Triển Khai

**Quy trình phát hành là gì?**

1. Danh sách kiểm tra trước triển khai
2. Các bước thực hiện triển khai
3. Xác thực sau triển khai
4. Thủ tục rollback (nếu cần)

## Di Chuyển Cơ Sở Dữ Liệu

**Chúng ta xử lý thay đổi schema như thế nào?**

- Chiến lược di chuyển
- Thủ tục sao lưu
- Cách tiếp cận rollback

## Quản Lý Bí Mật

**Chúng ta xử lý dữ liệu nhạy cảm như thế nào?**

- Biến môi trường
- Giải pháp lưu trữ bí mật
- Chiến lược xoay vòng khóa

## Kế Hoạch Rollback

**Nếu có gì đó sai sót thì sao?**

- Kích hoạt rollback
- Các bước rollback
- Kế hoạch giao tiếp
