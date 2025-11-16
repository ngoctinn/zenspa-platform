---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề
description: Làm rõ không gian vấn đề, thu thập yêu cầu và xác định tiêu chí thành công
---

# Yêu Cầu & Hiểu Vấn Đề

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

- Admin cần một cách hiệu quả để mời và quản lý nhân viên (Kỹ thuật viên, Lễ tân) vào hệ thống ZenSpa.
- Hiện tại, không có cơ chế để Admin chủ động thêm nhân viên mới hoặc gán vai trò bổ sung cho người dùng hiện tại.
- Vấn đề ảnh hưởng đến Admin, những người cần quản lý đội ngũ nhân viên một cách linh hoạt.
- Tình hình hiện tại: Admin phải phụ thuộc vào người dùng tự đăng ký và sau đó gán vai trò thủ công, hoặc không có cách nào để mời người dùng mới.

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

- Mục tiêu chính: Cho phép Admin mời nhân viên mới hoặc gán vai trò nhân viên cho người dùng hiện tại thông qua giao diện web.
- Mục tiêu phụ: Hỗ trợ nhiều vai trò cho một người dùng (ví dụ: Khách hàng kiêm Kỹ thuật viên).
- Không mục tiêu: Không bao gồm quản lý lương, lịch làm việc chi tiết, hoặc tích hợp với hệ thống HR bên ngoài.

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

- Là Admin, tôi muốn nhập email của một người và chọn vai trò (Kỹ thuật viên hoặc Lễ tân) để mời họ vào hệ thống.
- Là Admin, tôi muốn xem danh sách nhân viên với thông tin email, vai trò, và trạng thái tài khoản.
- Là người dùng mới được mời, tôi nhận email mời, nhấp vào link, tạo mật khẩu và có quyền hạn tương ứng.
- Là người dùng hiện tại được gán vai trò mới, tôi nhận email thông báo và có thể truy cập các chức năng mới khi đăng nhập.
- Quy trình làm việc chính: Admin → Nhập email + vai trò → Hệ thống kiểm tra → Gửi mời hoặc gán vai trò → Thông báo cho người dùng.
- Trường hợp biên: Email đã được mời nhưng chưa chấp nhận, gán trùng vai trò đã có.

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

- Admin có thể mời nhân viên mới thành công và họ nhận được email mời.
- Admin có thể gán vai trò bổ sung cho người dùng hiện tại và họ nhận được email thông báo.
- Người dùng mới có thể chấp nhận lời mời và truy cập với vai trò được gán.
- Người dùng hiện tại có thể truy cập các chức năng mới sau khi được gán vai trò.
- Hệ thống xử lý đúng các trường hợp: mời mới, gán cho hiện tại, trùng vai trò, đã mời.

## Ràng Buộc & Giả Định

**Chúng ta cần làm việc trong giới hạn nào?**

- Ràng buộc kỹ thuật: Sử dụng Supabase Auth cho quản lý người dùng, FastAPI cho backend, Next.js cho frontend.
- Ràng buộc kinh doanh: Chỉ Admin mới có quyền mời nhân viên, vai trò chỉ là Kỹ thuật viên và Lễ tân.
- Giả định: Email là duy nhất, Supabase xử lý việc gửi email mời, hệ thống có bảng user_roles để quản lý vai trò nhiều-nhiều.

## Câu Hỏi & Vấn Đề Mở

**Chúng ta vẫn cần làm rõ gì?**

- Chi tiết về template email mời và thông báo.
- Cách xử lý trường hợp người dùng từ chối lời mời hoặc xóa vai trò.
- Tích hợp với frontend để hiển thị vai trò động trong UI.
