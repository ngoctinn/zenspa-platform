```markdown
---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề
description: Làm rõ không gian vấn đề, thu thập yêu cầu và xác định tiêu chí thành công
---

# Yêu Cầu & Hiểu Vấn Đề - Nền tảng Dashboard Admin

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

- **Vấn đề cốt lõi:** Dự án thiếu một layout (bố cục) chung và nhất quán cho các trang quản trị. Việc này dẫn đến việc phải lặp lại code UI, khó bảo trì và trải nghiệm người dùng không đồng nhất giữa các trang.
- **Ai bị ảnh hưởng:** Các nhà phát triển (tốn thời gian xây dựng UI), và người dùng cuối (admin, lễ tân, kỹ thuật viên) phải làm quen với nhiều giao diện khác nhau.
- **Cách giải quyết hiện tại:** Chưa có. Mỗi trang quản trị mới sẽ phải tự xây dựng layout từ đầu.

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

- **Mục tiêu chính:** Xây dựng một bộ components layout nền tảng, có thể tái sử dụng cho toàn bộ các trang trong khu vực quản trị.
- **Mục tiêu phụ:**
  - Layout phải responsive, hoạt động tốt trên cả desktop và mobile.
  - Cung cấp cấu trúc rõ ràng với Sidebar (thanh bên) cho điều hướng và Navbar (thanh trên) cho thông tin người dùng và các hành động nhanh.
  - Dễ dàng mở rộng, cho phép thêm các mục menu mới mà không cần sửa đổi nhiều.
- **Không mục tiêu:**
  - Xây dựng hoàn chỉnh tất cả các trang quản trị chi tiết (như quản lý người dùng, quản lý lịch hẹn). Tính năng này chỉ tập trung vào layout nền tảng.
  - Thiết kế logic nghiệp vụ backend phức tạp.

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

- **Là một Quản trị viên,** tôi muốn thấy một thanh điều hướng bên cạnh (sidebar) với các mục menu rõ ràng (ví dụ: "Tổng quan", "Quản lý Lịch hẹn", "Quản lý Nhân viên") để tôi có thể di chuyển nhanh chóng giữa các trang quản lý.
- **Là một Nhân viên (lễ tân/kỹ thuật viên),** tôi muốn thấy tên và ảnh đại diện của mình trên thanh điều hướng trên cùng (navbar) để biết rằng tôi đang đăng nhập đúng tài khoản.
- **Là một người dùng trên thiết bị di động,** tôi muốn sidebar có thể ẩn/hiện để tiết kiệm không gian màn hình, và có thể truy cập menu thông qua một nút bấm.
- **Là một Nhà phát triển,** tôi muốn sử dụng một component `AdminPanelLayout` duy nhất để bao bọc các trang quản trị mới, giúp tôi xây dựng tính năng nhanh hơn mà không cần quan tâm đến UI xung quanh.

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

- Một trang quản trị mẫu (ví dụ: `/admin/dashboard`) được tạo ra và sử dụng thành công bộ components layout mới.
- Layout hiển thị chính xác trên các kích thước màn hình phổ biến (desktop, tablet, mobile).
- Sidebar chứa các mục menu có thể cấu hình được.
- Trạng thái đóng/mở của sidebar nên được lưu lại (ví dụ: dùng localStorage) để duy trì lựa chọn của người dùng trong các lần truy cập sau.
- Navbar hiển thị thông tin người dùng và có nút đăng xuất.
- Code của layout được tách thành các components rõ ràng, dễ hiểu và tái sử dụng (Sidebar, Navbar, ContentLayout, v.v.).

## Ràng Buộc & Giả Định

**Chúng ta cần làm việc trong giới hạn nào?**

- **Ràng buộc kỹ thuật:** Phải được xây dựng bằng Next.js, TypeScript, Tailwind CSS và Shadcn/UI theo đúng stack công nghệ của dự án.
- **Giả định:** Dữ liệu người dùng (tên, email, avatar) đã có thể lấy được từ API hoặc Supabase auth.

## Câu Hỏi & Vấn Đề Mở

**Chúng ta vẫn cần làm rõ gì?**

- Danh sách chính xác các mục menu ban đầu cho từng vai trò (admin, lễ tân, kỹ thuật viên) là gì? (Tạm thời có thể dùng danh sách giả định).
```
