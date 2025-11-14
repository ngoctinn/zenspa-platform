---
phase: testing
title: Chiến Lược Kiểm Tra
description: Xác định cách tiếp cận kiểm tra, trường hợp kiểm tra và đảm bảo chất lượng
---

# Chiến Lược Kiểm Tra

## Mục Tiêu Bao Phủ Kiểm Tra

**Chúng ta nhắm đến mức kiểm tra nào?**

- 100% cho layout logic.
- Integration với routing.

## Kiểm Tra Đơn Vị

**Thành phần riêng lẻ nào cần kiểm tra?**

### AccountLayout

- [ ] Render 2 columns
- [ ] Sidebar visible
- [ ] Content area flexible

### SidebarMenu

- [ ] Menu items render
- [ ] Click navigation

## Kiểm Tra Tích Hợp

**Chúng ta kiểm tra tương tác thành phần như thế nào?**

- [ ] Layout with public layout
- [ ] Navigation changes content

## Kiểm Tra End-to-End

**Luồng người dùng nào cần xác thực?**

- [ ] Login → Account page → Menu click → Content change

## Dữ Liệu Kiểm Tra

**Chúng ta sử dụng dữ liệu nào để kiểm tra?**

- Mock user data.

## Báo Cáo & Bao Phủ Kiểm Tra

**Chúng ta xác minh và giao tiếp kết quả kiểm tra như thế nào?**

- pnpm test --coverage

## Kiểm Tra Thủ Công

**Điều gì cần xác thực của con người?**

- Responsive trên mobile
- UI consistency

## Kiểm Tra Hiệu Suất

**Chúng ta xác thực hiệu suất như thế nào?**

- Load time check

## Theo Dõi Lỗi

**Chúng ta quản lý vấn đề như thế nào?**

- GitHub issues
