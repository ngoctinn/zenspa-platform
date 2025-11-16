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

- Là Admin, tôi muốn nhập email của một người và chọn vai trò (Kỹ thuật viên hoặc Lễ tân) để mời họ vào hệ thống. (Acceptance: Form validate email, dropdown role, button submit, toast "Đã gửi mời")
- Là Admin, tôi muốn xem danh sách nhân viên với thông tin email, vai trò, và trạng thái tài khoản. (Acceptance: Table/list hiển thị data từ API, filter/search)
- Là người dùng mới được mời, tôi nhận email mời (subject: "Mời tham gia ZenSpa", body: link accept, role info), nhấp vào link, tạo mật khẩu và có quyền hạn tương ứng. (Acceptance: Email gửi trong 5min, link valid 24h, login success)
- Là người dùng hiện tại được gán vai trò mới, tôi nhận email thông báo (subject: "Bạn đã được gán vai trò [role]", body: login để access). (Acceptance: Email gửi ngay, login thấy menu mới)
- Quy trình làm việc chính: Admin → Nhập email + vai trò → Hệ thống kiểm tra → Gửi mời hoặc gán vai trò → Thông báo cho người dùng.
- Trường hợp biên: Email đã được mời nhưng chưa chấp nhận (Acceptance: UI show "Đã mời, gửi lại?"), gán trùng vai trò đã có (Acceptance: Message "User đã có role này").

### Stakeholders & Priorities
- **Primary**: Admin (high priority, core user).
- **Secondary**: Staff users (technician, receptionist – medium priority).
- **Tertiary**: Existing customers getting new roles (low priority).

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

## Yêu Cầu Phi Chức Năng

**Hệ thống nên hoạt động như thế nào?**

- Hiệu suất: Email gửi trong 5 phút, API response < 2 giây.
- Bảo mật: JWT validation, input sanitization, chỉ Admin access.
- Độ tin cậy: Uptime 99%, error handling cho Supabase failures.
- Khả năng mở rộng: Hỗ trợ 1000 invites/tháng ban đầu.

## Câu Hỏi & Vấn Đề Mở

**Chúng ta vẫn cần làm rõ gì?**

- Chi tiết về template email mời (subject: "Mời tham gia ZenSpa với vai trò [role]", body: chào mừng, link accept, expire 24h) và thông báo (subject: "Vai trò [role] đã được gán", body: hướng dẫn login).
- Cách xử lý trường hợp người dùng từ chối lời mời (cancel invite) hoặc xóa vai trò (future feature).
- Tích hợp với frontend để hiển thị vai trò động trong UI (menu show/hide based on roles, e.g., if "admin" in roles show staff management).
- Error scenarios: Invalid email format (client validate), Supabase down (server error), email bounce (log and notify admin).
