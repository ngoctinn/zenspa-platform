---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề - Admin User Management
description: Làm rõ không gian vấn đề, thu thập yêu cầu và xác định tiêu chí thành công cho tính năng quản lý tài khoản người dùng
---

# Yêu Cầu & Hiểu Vấn Đề - Admin User Management

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

- Admin cần công cụ quản lý toàn diện tài khoản người dùng (khách hàng, nhân viên) trong hệ thống Spa
- Hiện tại admin phải quản lý thủ công qua database hoặc Supabase dashboard, thiếu giao diện thân thiện
- Cần phân quyền chi tiết và linh hoạt cho từng loại người dùng
- Thiếu khả năng khóa/mở tài khoản nhanh chóng khi có vấn đề

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

- Xây dựng giao diện quản lý tài khoản người dùng hoàn chỉnh cho admin
- Hỗ trợ phân quyền RBAC (Role-Based Access Control) với multi-role
- Đảm bảo bảo mật tuyệt đối, chỉ admin mới truy cập được
- Tối ưu UX để admin thao tác nhanh chóng và chính xác

**Không mục tiêu:**

- Không xây dựng tính năng tự phục vụ cho user (chỉ admin)
- Không tích hợp với hệ thống bên thứ ba
- Không hỗ trợ bulk operations phức tạp (chỉ CRUD cơ bản)

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

- Là Admin, tôi muốn xem danh sách tất cả tài khoản với thông tin: họ tên, email, sđt, trạng thái, roles hiện tại
- Là Admin, tôi muốn tạo mới tài khoản cho nhân viên mới qua email
- Là Admin, tôi muốn khóa/mở hoặc xóa tài khoản khi cần thiết
- Là Admin, tôi muốn đổi email đăng nhập cho nhân viên mà không mất dữ liệu hồ sơ
- Là Admin, tôi muốn gán/thu hồi một hoặc nhiều role cho tài khoản
- Là Admin, tôi muốn xem và chỉnh sửa thông tin hồ sơ bổ sung của user

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

- Admin có thể xem danh sách users với pagination và search
- Admin có thể tạo/sửa/xóa user account
- Admin có thể assign/unassign roles linh hoạt
- Tất cả actions có validation và error handling
- UI responsive và accessible
- Performance: load < 2s cho danh sách 100 users

## Ràng Buộc & Giả Định

**Chúng ta cần làm việc trong giới hạn nào?**

- Sử dụng Supabase Auth cho authentication
- Database schema đã có (profiles, roles, user_role_links)
- Frontend: Next.js 16+ với Shadcn/UI
- Backend: FastAPI với SQLModel
- Chỉ admin mới truy cập được tính năng này

## Câu Hỏi & Vấn Đề Mở

**Chúng ta vẫn cần làm rõ gì?**

- Cần xác nhận workflow tạo user: có gửi email invite không?
- Phân quyền chi tiết: admin có thể sửa profile của user khác không?
- Logging: cần audit trail cho các thay đổi quan trọng không?
