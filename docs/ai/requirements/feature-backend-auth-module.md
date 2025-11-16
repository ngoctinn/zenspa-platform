---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề
description: Làm rõ không gian vấn đề, thu thập yêu cầu và xác định tiêu chí thành công
feature: backend-auth-module
---

# Yêu Cầu & Hiểu Vấn Đề

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

- Backend FastAPI chưa có cơ chế verify JWT từ Supabase, dẫn đến APIs không được bảo mật server-side.
- Thiếu cách quản lý và enforce roles (customer, receptionist, technician, admin), khiến permissions không được kiểm soát.
- Admin không có API để gán roles cho nhân viên, phải manual qua Supabase Dashboard.
- Người dùng bị ảnh hưởng: Admin (khó manage roles), Staff (access không đúng), Customer (data không protected), Developers (phát triển chậm).
- Tình hình hiện tại: Frontend xử lý auth qua Supabase, nhưng backend trust client mà không verify.

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

- Mục tiêu chính: Backend verify JWT Supabase, extract roles, enforce permissions cho APIs.
- Mục tiêu phụ: Admin gán roles qua API backend, sync với Supabase metadata.
- Không mục tiêu: Implement auth UI, thay đổi frontend logic, self-manage login/signup.

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

- Là một admin, tôi muốn gán roles cho users qua API backend để permissions được update trong JWT.
- Là một backend developer, tôi muốn JWT verification middleware để APIs secure.
- Là một receptionist, tôi muốn role checked trong APIs để chỉ access appointment management.
- Là một customer, tôi muốn JWT verified cho profile APIs để personal data protected.
- Là một technician, tôi muốn role-based access đến medical notes để sensitive data không exposed.
- Là một developer, tôi want role extraction từ JWT để implement conditional logic.
- Là một admin, tôi want list users với roles để audit và manage permissions.

Quy trình: User login frontend → Supabase JWT → Backend verify → Extract role → Enforce API access.

Trường hợp biên: User không role (default customer), JWT expired (reject), admin gán role sai (validation).

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

- 100% APIs protected với JWT verify.
- Roles enforced (admin APIs block non-admin).
- Admin API gán roles hoạt động, update Supabase metadata.
- Tests pass (unit/integration), no security vulnerabilities.
- Performance: JWT verify <100ms.

## Ràng Buộc & Giả Định

**Chúng ta cần làm việc trong giới hạn nào?**

- Ràng buộc kỹ thuật: Chỉ verify Supabase JWT, không self-manage auth; dùng PyJWT, supabase-py.
- Ràng buộc kinh doanh: Roles đơn giản (4 types), không granular permissions.
- Ràng buộc thời gian: Implement trong 1-2 weeks.
- Giả định: Supabase metadata lưu role, JWKS endpoint ổn định; database PostgreSQL nếu cần audit.

## Câu Hỏi & Vấn Đề Mở

**Chúng ta vẫn cần làm rõ gì?**

- Cách handle role changes real-time (invalidate sessions?).
- Sync roles với DB nếu audit cần.
- Fallback nếu JWKS down.
