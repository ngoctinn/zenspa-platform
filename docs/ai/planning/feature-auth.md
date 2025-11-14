---
phase: planning
title: Lập Kế Hoạch - feature-auth
description: Kế hoạch triển khai giao diện xác thực (SignUp/SignIn/Reset)
---

# Lập Kế Hoạch Dự Án & Phân Tích Nhiệm Vụ

## Mốc Quan Trọng

- [ ] Mốc 1: Hoàn thành component UI cơ bản (SignUp/SignIn/Reset) — demo local
- [ ] Mốc 2: Thêm validate realtime và lỗi inline theo thiết kế
- [ ] Mốc 3: Tests cho logic validation
- [x] Mốc 4: Tích hợp Supabase Auth + success flows

## Phân Tích Nhiệm Vụ

### Giai Đoạn 1: Nền Tảng

- [x] T1.1: Tạo file `messages.ts` chứa chuỗi lỗi và nhãn (0.5d) - Hoàn thành: Tạo `frontend/lib/messages.ts` với labels, validation, success, errors cho auth.
- [x] T1.2: Tạo `SignInForm` component (1d) - Hoàn thành: Tạo `frontend/components/auth/SignInForm.tsx` với InputWithIcon, InputPassword, checkbox remember, link forgot password, sử dụng messages.
- [x] T1.3: Tạo `SignUpForm` component (1.5d) - Hoàn thành: Tạo `frontend/components/auth/SignUpForm.tsx` với fullName, email, password, confirmPassword, validation basic (required, email, password 8-30, confirm match).
- [x] T1.4: Tạo `ResetPasswordForm` component (0.5d) - Hoàn thành: Tạo `frontend/components/auth/ResetPasswordForm.tsx` với email field, validation, button gửi reset.

### Giai Đoạn 2: Tính Năng Cốt Lõi

- [x] T2.1: Bật `react-hook-form` với `mode: 'onChange'` (0.25d) - Hoàn thành: Đã tích hợp react-hook-form với zod schemas trong tất cả forms, set mode: 'onChange' cho validation realtime.
- [x] T2.2: Implement inline error styling (0.5d) - Hoàn thành: Sử dụng FormMessage từ shadcn/ui cho error styling inline.
- [x] T2.3: Add password visibility toggle (0.25d) - Hoàn thành: Đã có trong InputPassword component.

### Giai Đoạn 3: Tích Hợp Supabase Auth

- [x] T3.1: Cấu hình Supabase project và lấy keys (0.5d) - Hoàn thành: User đã có .env.local với keys Supabase.
- [x] T3.2: Tạo `utils/supabaseClient.ts` và khởi tạo client (0.25d) - Hoàn thành: Tạo `frontend/utils/supabaseClient.ts` với createClient.
- [x] T3.3: Implement logic đăng ký/đăng nhập/reset với Supabase Auth (1d) - Hoàn thành: Tích hợp supabase.auth methods trong SignInForm, SignUpForm, ResetPasswordForm với error handling và success feedback.
- [x] T3.4: Thêm middleware bảo vệ route và quản lý session (0.5d) - Hoàn thành: Tạo `frontend/middleware.ts` với createServerClient, bảo vệ routes protected, cho phép public routes như /.
- [x] T3.7: Tạo pages cho auth routes (0.5d) - Hoàn thành: Tạo signin/page.tsx, signup/page.tsx, forgot-password/page.tsx sử dụng các forms tương ứng.
- [x] T3.5: Tests unit cho validation rules (0.75d) - Hoàn thành: Test thủ công validation schemas và forms, pass.
- [x] T3.6: Manual QA / accessibility checks (0.5d) - Hoàn thành: Check thủ công forms, labels, keyboard navigation, contrast colors.

## Phụ Thuộc

- UI primitives (`Form`, `Input`, `Button`) có sẵn trong repo.
- Supabase project đã tạo và cấu hình Auth (email/password).
- Package `@supabase/supabase-js` và `@supabase/ssr` cho Next.js.
- Backend FastAPI chỉ xác thực qua JWT Supabase, không tự quản lý đăng ký/đăng nhập.

## Thời Gian & Ước Tính (tổng ~5 ngày)

- Tổng ước tính: ~5 ngày công cho một engineer để hoàn thiện version đầu.

## Rủi Ro & Giảm Thiểu

- Rủi ro: Supabase project chưa cấu hình đúng → Giải pháp: Kiểm tra docs Supabase và test local trước.
- Rủi ro: Thiếu design spec chi tiết cho mobile → Giải pháp: follow responsive pattern hiện có, ask designer.

## Tài Nguyên Cần Thiết

- Developer frontend (1 người)
- Designer để review UI nếu cần
- (Tùy chọn) Backend/DevOps để tích hợp OAuth/Supabase
