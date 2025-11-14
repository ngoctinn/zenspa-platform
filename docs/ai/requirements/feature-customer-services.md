---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề - feature-customer-services
description: Yêu cầu cho trang gói dịch vụ của khách hàng
---

# Yêu Cầu & Hiểu Vấn Đề

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

- Khách hàng cần xem và quản lý các gói dịch vụ/liệu trình đã mua (số lần sử dụng còn lại, chi tiết gói).
- Thiếu giao diện tập trung để theo dõi dịch vụ đã mua.

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

- Mục tiêu chính: Hiển thị danh sách gói dịch vụ với thông tin chi tiết (tên, mô tả, số lần còn lại, ngày hết hạn).
- Mục tiêu phụ: Cho phép mua thêm hoặc gia hạn gói.
- Không mục tiêu: Không tạo gói mới (chỉ xem/quản lý).

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

- Là khách hàng, tôi muốn xem các gói dịch vụ đã mua để biết còn sử dụng được bao nhiêu lần.
- Là khách hàng, tôi muốn mua thêm gói nếu hết.

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

- Trang hiển thị danh sách gói dịch vụ với progress bar cho số lần còn lại.
- Có nút mua thêm.
- Responsive và tuân thủ UI.

## Ràng Buộc & Giả Định

**Ràng buộc kỹ thuật**

- Sử dụng Shadcn/UI (Card, Progress, Button).
- Fetch từ Supabase.

**Giả định**

- Data services có sẵn.

## Câu Hỏi & Vấn Đề Mở

- Data structure cho services?
- Cách handle mua thêm (redirect to booking)?
