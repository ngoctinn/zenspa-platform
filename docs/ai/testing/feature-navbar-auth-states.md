---
phase: testing
title: Chiến Lược Kiểm Tra
description: Xác định cách tiếp cận kiểm tra, trường hợp kiểm tra và đảm bảo chất lượng
---

# Chiến Lược Kiểm Tra

## Mục Tiêu Bao Phủ Kiểm Tra

**Chúng ta nhắm đến mức kiểm tra nào?**

- 100% bao phủ cho component mới.

## Kiểm Tra Đơn Vị

**Thành phần riêng lẻ nào cần kiểm tra?**

### AuthActions

- [x] Test render nút Đăng nhập và Đăng ký.

### NotificationIcon

- [x] Test badge hiển thị số lượng.

### UserProfileMenu

- [x] Test dropdown mở và các liên kết.

### Navbar

- [x] Test conditional render: AuthActions khi chưa đăng nhập, NotificationIcon + UserProfileMenu khi đã đăng nhập.

## Kiểm Tra Tích Hợp

**Chúng ta kiểm tra tương tác thành phần như thế nào?**

- [ ] Kịch bản tích hợp 1
- [ ] Kịch bản tích hợp 2
- [ ] Kiểm tra điểm cuối API
- [ ] Kiểm tra tích hợp 3 (chế độ thất bại / rollback)

## Kiểm Tra End-to-End

**Luồng người dùng nào cần xác thực?**

- [ ] Luồng người dùng 1: [Mô tả]
- [ ] Luồng người dùng 2: [Mô tả]
- [ ] Kiểm tra đường dẫn quan trọng
- [ ] Hồi quy của các tính năng liền kề

## Dữ Liệu Kiểm Tra

**Chúng ta sử dụng dữ liệu nào để kiểm tra?**

- Bộ dữ liệu kiểm tra và mô phỏng
- Yêu cầu dữ liệu hạt giống
- Thiết lập cơ sở dữ liệu kiểm tra

## Báo Cáo & Bao Phủ Kiểm Tra

**Chúng ta xác minh và giao tiếp kết quả kiểm tra như thế nào?**

- Lệnh bao phủ và ngưỡng (`npm run test -- --coverage`)
- Khoảng trống bao phủ (tệp/chức năng dưới 100% và lý do)
- Liên kết đến báo cáo hoặc bảng điều khiển kiểm tra
- Kết quả kiểm tra thủ công và ký duyệt

## Kiểm Tra Thủ Công

**Điều gì cần xác nhận của con người?**

- Danh sách kiểm tra kiểm tra UI/UX (bao gồm khả năng truy cập)
- Tương thích trình duyệt/thiết bị
- Kiểm tra khói sau triển khai

## Kiểm Tra Hiệu Suất

**Chúng ta xác thực hiệu suất như thế nào?**

- Kịch bản kiểm tra tải
- Cách tiếp cận kiểm tra căng thẳng
- Điểm chuẩn hiệu suất

## Theo Dõi Lỗi

**Chúng ta quản lý vấn đề như thế nào?**

- Quy trình theo dõi vấn đề
- Mức độ nghiêm trọng lỗi
- Chiến lược kiểm tra hồi quy
