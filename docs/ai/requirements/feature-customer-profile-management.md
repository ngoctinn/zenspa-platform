---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề
description: Làm rõ không gian vấn đề, thu thập yêu cầu và xác định tiêu chí thành công
---

# Yêu Cầu & Hiểu Vấn Đề

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

- Dữ liệu profile của khách hàng (như số điện thoại, ngày sinh) không nằm trong auth.users (metadata) của Supabase, mà cần được lưu trữ ở một bảng riêng trong database để quản lý.
- Khách hàng bị ảnh hưởng vì không thể cập nhật thông tin cá nhân đầy đủ sau đăng ký.
- Tình hình hiện tại: Chỉ lưu metadata trong Supabase, không có DB backend riêng cho profile mở rộng.

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

- Mục tiêu chính: Cho phép khách hàng quản lý profile đầy đủ (tạo tự động, xem, cập nhật, upload avatar).
- Mục tiêu phụ: Tích hợp Supabase Auth Hooks để sync profile ngay khi signup.
- Không mục tiêu: Không quản lý profile cho staff/admin, không tích hợp với bên thứ ba ngoài Supabase.

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

- Story 1 (Tạo profile): Là một customer, tôi muốn profile của mình (với email, họ tên) được tự động tạo ngay sau khi đăng ký (signup) để tôi không phải nhập lại thông tin.
- Story 2 (Xem profile): Là một customer, tôi muốn xem thông tin profile của mình (họ tên, SĐT, ngày sinh, avatar) khi tôi truy cập trang "Tài khoản" để xác nhận thông tin.
- Story 3 (Cập nhật profile): Là một customer, tôi muốn cập nhật thông tin cá nhân (như SĐT, ngày sinh) để spa có thông tin liên lạc chính xác.
- Story 4 (Cập nhật avatar): Là một customer, tôi muốn tải lên hoặc thay đổi ảnh đại diện (avatar) để cá nhân hóa tài khoản của mình.
- Quy trình: Signup → Auto create profile → Login → View/Update profile.
- Trường hợp biên: User chưa có profile (fallback create), update fail (error handling).

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

- Profile tự động tạo sau signup (100% user có profile).
- Frontend hiển thị và cho phép update profile đầy đủ.
- API GET/PUT /me hoạt động với validation.
- Avatar upload thành công và hiển thị.
- Điểm chuẩn: Response time < 500ms cho API.

## Ràng Buộc & Giả Định

**Chúng ta cần làm việc trong giới hạn nào?**

- Ràng buộc kỹ thuật: Sử dụng Supabase DB + Auth Hooks, FastAPI backend, Next.js frontend.
- Ràng buộc kinh doanh: Chỉ cho customer, không thay đổi auth flow.
- Ràng buộc thời gian: Hoàn thành trong 1-2 tuần.
- Giả định: Supabase account đã setup, user metadata có full_name.

## Câu Hỏi & Vấn Đề Mở

**Chúng ta vẫn cần làm rõ gì?**

- Cần confirm Supabase Auth Hooks có support Postgres Function không?
- Cách handle avatar storage (Supabase Storage vs local).
- Validation cho phone/birth_date format.
