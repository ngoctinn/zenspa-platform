---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề
description: Làm rõ không gian vấn đề, thu thập yêu cầu và xác định tiêu chí thành công
---

# Yêu Cầu & Hiểu Vấn Đề

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

- Navbar hiện tại chỉ hiển thị CTA (Đăng nhập/Đăng ký) cho khách vãng lai, thiếu hoàn toàn giao diện và chức năng (như Thông báo, Profile) cho khách hàng đã đăng nhập, dẫn đến trải nghiệm không nhất quán và thiếu tính năng cần thiết.
- Khách hàng đã đăng nhập không có cách truy cập nhanh vào thông báo, hồ sơ cá nhân, hoặc đăng xuất, gây khó khăn trong việc quản lý tài khoản.
- Ai bị ảnh hưởng: Tất cả khách hàng truy cập website ZenSpa, đặc biệt là khách hàng thành viên đã đăng nhập.
- Tình hình hiện tại: Navbar chỉ có nút Đăng nhập và Đăng ký, không phân biệt trạng thái đăng nhập.

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

- Mục tiêu chính: Cung cấp trải nghiệm nhất quán và đầy đủ cho cả khách vãng lai và khách hàng thành viên trong Navbar.
- Mục tiêu phụ: Tách riêng các component để dễ tái sử dụng và bảo trì, tránh code lặp lại trong Navbar.tsx.
- Không mục tiêu: Không tích hợp backend API cho thông báo hoặc profile trong phase này; chỉ thay đổi UI frontend.

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

- Là một khách vãng lai, tôi muốn thấy nút 'Đăng nhập' và 'Đăng ký' để có thể tham gia hệ thống.
- Là một khách hàng đã đăng nhập, tôi muốn thấy tên/avatar của mình và icon 'Thông báo' (kèm số lượng) để biết khi có lịch hẹn được xác nhận hoặc khuyến mãi mới.
- Là một khách hàng đã đăng nhập, khi nhấp vào tên/avatar, tôi muốn thấy một menu thả xuống (dropdown) với các liên kết: Hồ sơ của tôi, Lịch hẹn của tôi, và Đăng xuất.
- Quy trình làm việc: Khi chưa đăng nhập, hiển thị CTA. Khi đăng nhập, thay thế bằng thông báo và menu profile. Dropdown có các liên kết điều hướng.
- Trường hợp biên: Người dùng chưa có avatar (hiển thị tên hoặc icon mặc định); số lượng thông báo = 0 (ẩn badge).

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

- Navbar hiển thị đúng CTA cho trạng thái chưa đăng nhập.
- Navbar hiển thị icon thông báo với badge và menu profile cho trạng thái đã đăng nhập.
- Dropdown menu có các liên kết: Hồ sơ, Lịch hẹn, Đăng xuất.
- Các component được tách riêng và tái sử dụng được.
- UI responsive và tuân thủ design system (Shadcn/UI, Tailwind).

## Ràng Buộc & Giả Định

**Chúng ta cần làm việc trong giới hạn nào?**

- Ràng buộc kỹ thuật: Sử dụng Next.js, TypeScript, Shadcn/UI; không thay đổi backend.
- Ràng buộc kinh doanh: Phải tuân thủ quy tắc dự án ZenSpa (tiếng Việt, không hardcode).
- Giả định: Trạng thái đăng nhập được quản lý qua Supabase auth; dữ liệu user (tên, avatar) có sẵn.

## Câu Hỏi & Vấn Đề Mở

**Chúng ta vẫn cần làm rõ gì?**

- Cách lấy số lượng thông báo chưa đọc từ backend?
- Dữ liệu user (tên, avatar) được lưu trữ như thế nào trong Supabase?
- Cần tích hợp real-time cho thông báo không?
