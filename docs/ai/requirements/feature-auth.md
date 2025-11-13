---
feature: auth
phase: requirements
---

# Requirements: Authentication System

## Problem Statement

Hệ thống ZenSpa hiện tại chưa có giao diện và logic xác thực người dùng. Người dùng cần có khả năng đăng ký tài khoản mới, đăng nhập vào hệ thống, và khôi phục mật khẩu khi quên để truy cập các tính năng quản lý lịch hẹn, liệu trình, nhân viên và khách hàng.

## Goals

- Triển khai đầy đủ luồng đăng ký, đăng nhập, quên mật khẩu với email/password sử dụng Supabase Auth.
- Giao diện responsive, thân thiện với người dùng Việt, hỗ trợ mobile/desktop.
- Validation realtime, thông báo lỗi cụ thể bằng tiếng Việt.
- Tích hợp an toàn với Supabase, gửi JWT cho backend.

## Non-Goals

- Xác thực đa yếu tố (MFA).
- Đăng nhập bằng mạng xã hội (Google, Facebook).
- Quản lý vai trò người dùng (role-based access control) - chỉ xác thực cơ bản.

## User Stories

- Là khách hàng Spa, tôi muốn đăng ký tài khoản để đặt lịch hẹn trực tuyến.
- Là nhân viên Spa, tôi muốn đăng nhập để quản lý lịch hẹn và khách hàng.
- Là người dùng quên mật khẩu, tôi muốn khôi phục mật khẩu qua email để tiếp tục sử dụng hệ thống.

## Success Criteria

- Người dùng có thể đăng ký tài khoản mới với email/password.
- Người dùng có thể đăng nhập thành công sau khi xác nhận email.
- Người dùng có thể khôi phục mật khẩu qua email.
- Giao diện hoạt động trên mobile và desktop, với thông báo bằng tiếng Việt.
- Tất cả form có validation realtime và loading states.

## Constraints & Assumptions

- Sử dụng Supabase Auth cho xác thực.
- Email xác nhận được gửi qua Supabase (hoặc SMTP tùy chỉnh).
- Frontend sử dụng Next.js với @supabase/ssr.
- Backend chỉ xác thực JWT từ Supabase, không xử lý đăng nhập.

## Open Questions

- Cần cấu hình SMTP cho email production?
- URL redirect sau xác nhận email là gì?
