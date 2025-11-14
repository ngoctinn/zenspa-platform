---
phase: testing
title: Chiến Lược Kiểm Tra
description: Xác định cách tiếp cận kiểm tra, trường hợp kiểm tra và đảm bảo chất lượng
---

# Chiến Lược Kiểm Tra

## Mục Tiêu Bao Phủ Kiểm Tra

**Chúng ta nhắm đến mức kiểm tra nào?**

- 100% cho components mới.

## Kiểm Tra Đơn Vị

**Thành phần riêng lẻ nào cần kiểm tra?**

### HeroSection

- [ ] Render đúng nội dung.
- [ ] CTA button hoạt động.

### ServicesBlock

- [ ] Hiển thị danh sách dịch vụ.

## Kiểm Tra Tích Hợp

**Chúng ta kiểm tra tương tác thành phần như thế nào?**

- [ ] Form submit to API.

## Kiểm Tra End-to-End

**Luồng người dùng nào cần xác thực?**

- [ ] Đặt lịch từ mobile.

## Dữ Liệu Kiểm Tra

**Chúng ta sử dụng dữ liệu nào để kiểm tra?**

- Mock data cho services.

## Báo Cáo & Bao Phủ Kiểm Tra

**Chúng ta xác minh và giao tiếp kết quả kiểm tra như thế nào?**

- pnpm test.

## Kiểm Tra Thủ Công

**Điều gì cần xác thực của con người?**

- Responsive trên mobile.

## Kiểm Tra Hiệu Suất

**Chúng ta xác thực hiệu suất như thế nào?**

- Load time <3s.

## Theo Dõi Lỗi

**Chúng ta quản lý vấn đề như thế nào?**

- GitHub issues.
