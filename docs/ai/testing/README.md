---
phase: testing
title: Chiến Lược Kiểm Tra
description: Xác định cách tiếp cận kiểm tra, trường hợp kiểm tra và đảm bảo chất lượng
---

# Chiến Lược Kiểm Tra

## Mục Tiêu Bao Phủ Kiểm Tra

**Chúng ta nhắm đến mức kiểm tra nào?**

- Mục tiêu bao phủ kiểm tra đơn vị (mặc định: 100% mã mới/thay đổi)
- Phạm vi kiểm tra tích hợp (đường dẫn quan trọng + xử lý lỗi)
- Kịch bản kiểm tra end-to-end (hành trình người dùng chính)
- Căn chỉnh với tiêu chí chấp nhận yêu cầu/thiết kế

## Kiểm Tra Đơn Vị

**Thành phần riêng lẻ nào cần kiểm tra?**

### Thành Phần/Mô-đun 1

- [ ] Trường hợp kiểm tra 1: [Mô tả] (bao phủ kịch bản / nhánh)
- [ ] Trường hợp kiểm tra 2: [Mô tả] (bao phủ trường hợp biên / xử lý lỗi)
- [ ] Bao phủ bổ sung: [Mô tả]

### Thành Phần/Mô-đun 2

- [ ] Trường hợp kiểm tra 1: [Mô tả]
- [ ] Trường hợp kiểm tra 2: [Mô tả]
- [ ] Bao phủ bổ sung: [Mô tả]

## Kiểm Tra Tích Hợp

**Chúng ta kiểm tra tương tác thành phần như thế nào?**

- [ ] Kịch bản tích hợp 1
- [ ] Kịch bản tích hợp 2
- [ ] Kiểm tra điểm cuối API
- [ ] Kịch bản tích hợp 3 (chế độ thất bại / rollback)

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

**Điều gì cần xác thực của con người?**

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
