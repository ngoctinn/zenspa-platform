---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề - feature-auth
description: Yêu cầu cho tính năng giao diện xác thực (đăng ký/đăng nhập/quên mật khẩu)
---

# Yêu Cầu & Hiểu Vấn Đề

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

- Cung cấp giao diện đăng ký, đăng nhập và quên mật khẩu cho khách hàng Spa.
- Giao diện cần validate realtime (onChange) để người dùng thấy lỗi ngay khi nhập sai.
- Giao diện cần thân thiện, responsive, hỗ trợ keyboard (tab/enter), và tuân thủ quy ước giao diện dự án (không hardcode màu/phông).

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

- Mục tiêu chính

  - Cung cấp form đăng ký, đăng nhập, quên mật khẩu hoạt động tốt trên desktop/mobile với validate realtime.
  - Hiển thị lỗi inline (viền đỏ, label đỏ, text lỗi màu đỏ) ngay khi người dùng nhập dữ liệu không hợp lệ.
  - Hỗ trợ hiển thị/ẩn mật khẩu và đăng nhập bằng Google.
  - Sau đăng nhập thành công, redirect đến `/dashboard`.

- Mục tiêu phụ

  - Dễ tái sử dụng: tách component form (SignUp/SignIn/Reset) để dùng ở trang modal hoặc trang độc lập.
  - Các thông báo/chuỗi hiển thị đặt trong file `consts`/i18n nhằm tránh hardcode.

- Không mục tiêu
  - Không tích hợp xác thực backend thật ngay trong bước này (chỉ mock API hoặc trả về success giả lập).
  - Không xử lý xác thực OAuth server-side (chỉ hiển thị nút Google; tích hợp OAuth thực tế là 1 task riêng).

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

- Là khách hàng, tôi muốn đăng ký bằng email để tạo tài khoản.
- Là khách hàng, tôi muốn nhận lỗi khi nhập sai để sửa ngay.
- Là khách hàng, tôi muốn xem/ẩn mật khẩu khi nhập để tránh sai.
- Là khách hàng, tôi muốn nhận email lấy lại mật khẩu khi quên.

Quy trình chính

- Trang/Modal đăng ký: nhập tên hiển thị, email, mật khẩu, xác nhận mật khẩu → validate onChange → submit (mock) → show success dialog.
- Trang/Modal đăng nhập: email + mật khẩu / nút Google → validate onChange → submit → redirect `/dashboard` on success.
- Trang quên mật khẩu: nhập email → validate onChange → gửi email lại (mock) → show confirmation.

Trường hợp biên cần xem xét

- Email không hợp lệ (kiểu `asdf`), hiển thị lỗi ngay.
- Mật khẩu ngắn hoặc không đủ yêu cầu, hiển thị lỗi rõ ràng.
- Xác nhận mật khẩu không khớp — lỗi hiện ngay khi khác.
- Submit khi trường còn lỗi (không được gửi).

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

- Giao diện SignUp/SignIn/Reset hoạt động trên desktop và mobile.
- Tất cả validate chạy `onChange` và hiển thị lỗi inline giống thiết kế (viền đỏ + label đỏ + text lỗi dưới input).
- Các nút (hiện/ẩn mật khẩu, Google) hoạt động như UI; Google có thể là mock.
- Sau đăng nhập (mock success), redirect đến `/dashboard`.
- Chuỗi hiển thị lỗi và nhãn được đặt trong file `frontend/components/auth/messages.ts` (không hardcode).
- Có test unit cho logic validation (ít nhất cho các rule chính).

## Ràng Buộc & Giả Định

**Ràng buộc kỹ thuật**

- Frontend sử dụng Next.js App Router + React + react-hook-form.
- Sử dụng component UI hiện có (`Form` primitives, `Input`, `Button`, `Label`).

**Giả định**

- Backend chưa sẵn sàng → sử dụng mock API/handler để mô phỏng thành công/thất bại.
- Ngôn ngữ hiển thị: Tiếng Việt (toàn bộ text).
- Styling tuân thủ biến theme (không hardcode màu/phông) — sử dụng class tailwind/variables hiện có.

## Câu Hỏi & Vấn Đề Mở

- Có cần tích hợp OAuth Google thật ngay bây giờ hay chỉ hiển thị nút (mock)?
- URL redirect sau đăng nhập là `/dashboard` đúng không? (đã ghi theo yêu cầu)
- Có thêm quy tắc mật khẩu khác (ký tự đặc biệt, ký tự hoa) hay chỉ yêu cầu chữ + số và độ dài 8–20?
- Có yêu cầu về test coverage cụ thể không? (mặc định: test cho logic validation mới)
