---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề
description: Làm rõ không gian vấn đề, thu thập yêu cầu và xác định tiêu chí thành công
feature: backend-user-profile-api
---

# Yêu Cầu & Hiểu Vấn Đề

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

- Backend FastAPI chưa có API endpoint để user đã đăng nhập lấy thông tin profile của mình từ JWT Supabase.
- Frontend cần gọi API để hiển thị profile (email, role, ID), nhưng hiện tại chỉ có dependency get_current_user nội bộ.
- Người dùng bị ảnh hưởng: Developers phải implement manual, UI không có data profile.
- Tình hình hiện tại: Chỉ có auth verify, chưa có public API để expose user info.

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

- Mục tiêu chính: Tạo API GET /api/v1/users/me để trả về thông tin user từ JWT.
- Mục tiêu phụ: Integrate với auth module, return id, email, role.
- Không mục tiêu: Update profile, self-manage user data (chỉ read từ JWT).

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

- Là một user đã login, tôi muốn gọi API GET /api/v1/users/me để lấy profile info (id, email, role) để hiển thị trên UI.
- Quy trình: User login frontend → Gửi JWT → Backend verify → Return user info.
- Trường hợp biên: JWT invalid (401), user không role (default customer).

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

- API GET /api/v1/users/me hoạt động, return JSON với id, email, role.
- Tests pass, integration với auth module.
- Performance: <100ms response.

## Ràng Buộc & Giả Định

**Chúng ta cần làm việc trong giới hạn nào?**

- Ràng buộc kỹ thuật: Sử dụng get_current_user dependency, không query DB.
- Ràng buộc kinh doanh: Chỉ read info từ JWT, không edit.
- Ràng buộc thời gian: Implement trong 1-2 hours.
- Giả định: JWT chứa user_metadata với role.

## Câu Hỏi & Vấn Đề Mở

**Chúng ta vẫn cần làm rõ gì?**

- Cần return thêm fields nào (e.g., full_name)?
- Handle nếu JWT expired?
