---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề - Auth Backend Module
description: Làm rõ không gian vấn đề, thu thập yêu cầu và xác định tiêu chí thành công
feature: auth-backend
---

# Yêu Cầu & Hiểu Vấn Đề - Auth Backend Module

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

Hệ thống ZenSpa cần một module xác thực và phân quyền đáng tin cậy ở backend để:

- Xác minh danh tính người dùng từ Supabase Auth
- Quản lý vai trò (customer, receptionist, technician, admin) với khả năng multi-role
- Bảo vệ các API endpoints theo vai trò nghiệp vụ cụ thể
- Theo dõi hoạt động quan trọng và security events (audit log)

**Ai bị ảnh hưởng bởi vấn đề này?**

- **Khách hàng (Customer):** Người dùng cuối, cần đăng nhập để xem dịch vụ, đặt/hủy lịch hẹn, quản lý hồ sơ cá nhân và lịch sử liệu trình
- **Lễ tân (Receptionist):** Nhân viên vận hành, cần xác thực để xử lý lịch hẹn tổng thể, check-in/out, cập nhật hồ sơ khách hàng và thanh toán
- **Kỹ thuật viên (Technician):** Nhân viên thực hiện dịch vụ, cần xác thực để xem lịch phân công, cập nhật trạng thái hẹn và ghi chú y tế nhạy cảm
- **Quản trị viên (Admin):** Vai trò cao cấp, cần phân quyền để quản lý toàn hệ thống, báo cáo kinh doanh, cấu hình dịch vụ và tài khoản nhân viên
- **Developers:** Cần API bảo mật, dễ tích hợp với phân quyền chi tiết

**Tình hình hiện tại:**

- Chưa có hệ thống phân quyền trong backend
- Supabase Auth xử lý đăng ký/đăng nhập (frontend)
- Backend chưa verify JWT và kiểm tra roles
- Không có audit trail cho security compliance

## Mục Tiêu & Mục Đích

**Mục tiêu chính:**

1. **Xác thực an toàn:** Verify JWT từ Supabase với public key
2. **Phân quyền linh hoạt:** Support multi-role (1 user có nhiều roles)
3. **Audit log:** Theo dõi login/logout và role changes
4. **Developer-friendly:** API rõ ràng, dễ bảo vệ endpoints

**Mục tiêu phụ:**

- Auto-assign role `customer` cho user mới đăng ký
- Middleware xác thực tự động cho protected routes
- Caching user info để giảm DB queries
- Error handling rõ ràng (401, 403, 404)

**Không mục tiêu (out of scope):**

- ❌ Không xử lý đăng ký/đăng nhập (Supabase Auth đảm nhận)
- ❌ Không quản lý password (Supabase xử lý)
- ❌ Không implement OAuth providers (Supabase có sẵn)
- ❌ Không xây dựng UI auth pages (frontend đã có)

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**User Stories Chính:**

### US-1: Verify JWT Token

**Là developer**, tôi muốn backend tự động verify JWT từ Supabase để đảm bảo chỉ user hợp lệ mới truy cập API.

**Acceptance Criteria:**

- [ ] Backend decode JWT từ header `Authorization: Bearer <token>`
- [ ] Verify signature với Supabase public key
- [ ] Extract `user_id`, `email`, `role` từ JWT payload
- [ ] Trả về 401 nếu token invalid/expired
- [ ] Cache decoded token để tránh verify lặp lại

### US-2: Role-Based Authorization

**Là developer**, tôi muốn protect endpoints theo role nghiệp vụ để đảm bảo phân quyền chính xác (VD: customer không thể access receptionist endpoints, technician không xem được payment).

**Acceptance Criteria:**

- [ ] Dependency `require_customer()` chỉ cho phép customer
- [ ] Dependency `require_receptionist()` chỉ cho phép lễ tân
- [ ] Dependency `require_technician()` chỉ cho phép kỹ thuật viên
- [ ] Dependency `require_admin()` chỉ cho phép admin
- [ ] Dependency `require_roles([receptionist, admin])` cho multi-role check
- [ ] Trả về 403 với message rõ ràng nếu user không có quyền

### US-3: Get Current User Info

**Là frontend developer**, tôi muốn endpoint `GET /api/v1/auth/me` để lấy thông tin user đã đăng nhập.

**Acceptance Criteria:**

- [ ] Trả về `user_id`, `email`, `roles[]`, `created_at`
- [ ] Include profile info nếu có (full_name, avatar_url)
- [ ] Trả về 401 nếu chưa đăng nhập
- [ ] Response time < 100ms (với caching)

### US-4: Auto-Assign Customer Role for All Users

**Là user mới hoặc admin**, khi tài khoản được tạo, hệ thống tự động gán role `customer` để user có thể sử dụng public area (xem dịch vụ, đặt lịch).

**Acceptance Criteria:**

- [ ] Supabase trigger/webhook gọi backend khi user mới được tạo
- [ ] Backend tạo record trong `profiles` table
- [ ] Backend tạo record trong `user_roles` với role=`customer` (không bao giờ bỏ qua)
- [ ] Xử lý idempotent (không duplicate nếu gọi nhiều lần)
- [ ] Nếu admin sau đó gán thêm role `receptionist` hoặc `technician`, user sẽ có [customer, receptionist] hoặc [customer, technician]
- [ ] **Login behavior:** Backend check role khi user đăng nhập
  - Có receptionist OR technician? → Redirect Admin Dashboard (làm việc)
  - Chỉ có customer? → ở Public Area (khách hàng bình thường)

### US-5: Audit Log for Security Events

**Là admin**, tôi muốn xem log các sự kiện bảo mật và nghiệp vụ quan trọng để giám sát hệ thống và compliance.

**Acceptance Criteria:**

**Security events:**

- [ ] Log event `user.login` khi user đăng nhập thành công
- [ ] Log event `user.logout` khi user đăng xuất
- [ ] Log event `role.assigned` khi admin gán role cho user
- [ ] Log event `role.revoked` khi admin xóa role của user

**Business-critical events:**

- [ ] Log event `appointment.checkin` khi receptionist check-in khách hàng
- [ ] Log event `medical_note.created` khi technician tạo medical note
- [ ] Log event `medical_note.updated` khi technician cập nhật medical note
- [ ] Log event `payment.processed` khi receptionist xử lý thanh toán
- [ ] Log event `payment.refunded` khi admin thực hiện refund
- [ ] Log event `service.configured` khi admin cấu hình dịch vụ

**Log structure:**

- [ ] Mỗi log có: `user_id`, `event_type`, `timestamp`, `ip_address`, `user_agent`, `metadata` (JSONB)
- [ ] Metadata chứa context cụ thể (VD: appointment_id, payment_amount, customer_id)
- [ ] Retention policy: Tất cả audit logs lưu tối thiểu 1 năm (unified policy)

### US-6: Multi-Role Support

**Là admin**, tôi muốn gán nhiều role cho 1 user (VD: vừa receptionist vừa technician) để linh hoạt phân quyền.

**Acceptance Criteria:**

- [ ] Bảng `user_roles` hỗ trợ many-to-many (1 user nhiều records)
- [ ] Unique constraint `(user_id, role)` tránh duplicate
- [ ] API check "user có ít nhất 1 trong các roles X"
- [ ] Endpoint `POST /api/v1/auth/roles` để admin assign role

### US-7: Fine-Grained Role Permissions

**Là admin**, tôi muốn phân quyền chi tiết theo vai trò nghiệp vụ để đảm bảo mỗi vai trò chỉ truy cập chức năng phù hợp với trách nhiệm.

**Acceptance Criteria:**

**Quyền hạn theo vai trò:**

- [ ] **Customer:** Xem dịch vụ, đặt/hủy/xem lịch hẹn, xem hồ sơ cá nhân, xem lịch sử thanh toán của chính mình (KHÔNG access tài chính tổng thể)
- [ ] **Receptionist:** Quản lý lịch hẹn (thêm/sửa/hủy), check-in/out, xem/cập nhật hồ sơ khách hàng, xử lý thanh toán (+ customer permissions)
- [ ] **Technician:** Xem lịch phân công cá nhân, cập nhật trạng thái appointment, ghi/xem medical notes (chỉ đọc/ghi, không xóa), xem hồ sơ khách hàng (+ customer permissions)
- [ ] **Technician KHÔNG có quyền:** Xem payment history, access tài chính (báo cáo, refund), quản lý users/roles, xem hồ sơ nhân viên khác
- [ ] **Admin:** Full quyền - quản lý users/roles/permissions, báo cáo tài chính, cấu hình dịch vụ, override/refund payments, xem audit logs (+ all)

**API Implementation:**

- [ ] Endpoint `GET /api/v1/auth/me` trả về user roles + permissions list
- [ ] Middleware check role TRƯỚC khi route handler được gọi
- [ ] Error 403 với message rõ ràng (không phải 401) khi user không có quyền
- [ ] Permission matrix được documented trong README hoặc postman collection

## Tiêu Chí Thành Công

**Kết quả có thể đo lường:**

1. ✅ **Security:** 100% protected endpoints verify JWT correctly
2. ✅ **Performance:** Auth middleware < 50ms overhead per request
3. ✅ **Coverage:** 100% test coverage cho auth module
4. ✅ **Audit:** Tất cả security events được log đầy đủ

**Tiêu chí chấp nhận:**

- [ ] Tất cả 7 user stories đạt acceptance criteria
- [ ] API docs đầy đủ cho auth endpoints (bao gồm role-specific permissions)
- [ ] Integration tests pass cho auth flows (test cả 4 roles)
- [ ] Security review không phát hiện vulnerabilities
- [ ] Permission matrix documented rõ ràng (role → allowed actions)

**Điểm chuẩn hiệu suất:**

- JWT verification: < 10ms (without network call)
- Get current user: < 100ms (with DB query + cache)
- Role check: < 5ms (in-memory after loading user)
- Audit log write: async, không chặn request

## Ràng Buộc & Giả Định

**Ràng buộc kỹ thuật:**

- Backend: Python 3.12+, FastAPI, SQLModel sync mode
- Database: Supabase PostgreSQL (phải tương thích với RLS policies)
- Auth Provider: Supabase Auth (không thể thay đổi)
- Type hints: Dùng `X | None` (Python 3.13+), không dùng `Optional`

**Ràng buộc kinh doanh:**

- Phải tuân thủ GDPR/data privacy (audit log có PII)
- Audit logs phải lưu tối thiểu 1 năm (unified retention policy)
- Role changes chỉ admin mới được thực hiện
- **Medical notes security:**
  - Medical notes chỉ technician và admin có quyền truy cập (đọc/ghi)
  - Database encryption at rest được bật (Supabase default)
  - Không cần application-level encryption (simplified approach)
- **Payment permissions:**
  - Payment processing chỉ receptionist và admin có quyền
  - Technician KHÔNG được xem payment history (principle of least privilege)
  - Admin có quyền override/refund payments (ghi nhận trên hệ thống, chuyển tiền thực có thể thủ công)
- **Role assignment:**
  - Admin gán role thủ công cho nhân viên mới (không tự động)
  - Không cần approval workflow (immediate effect)
  - Primary role: Role đầu tiên được gán sẽ là default landing page

**Giả định:**

- Supabase Auth đã setup sẵn (users table tồn tại)
- JWT payload có `user_id`, `email` (Supabase default)
- Network latency tới Supabase < 50ms
- Redis available cho caching (graceful fallback nếu down)

## Câu Hỏi & Vấn Đề Mở

**Câu hỏi đã được làm rõ (Clarifications):**

1. ✅ **Default Role Strategy:** **Tất cả users tự động được gán role `customer` khi được tạo** (via Supabase webhook → backend):

   - User mới đăng ký: Tự động có role `customer`
   - Admin tạo tài khoản staff: Tự động có role `customer` + Admin gán thêm `receptionist` hoặc `technician` (multi-role)
   - Kết quả: User có thể [customer], [customer + receptionist], [customer + technician], hoặc [customer + admin]

2. ✅ **Staff Assignment Flow:** Admin tạo tài khoản → Backend tự động assign `customer` → Admin gán thêm `receptionist` / `technician` → User có 2 roles

3. ✅ **Login Redirect Logic:** Backend check role khi user đăng nhập:

   - **Nếu user có receptionist OR technician role:** Redirect tới Admin Dashboard (làm việc)
   - **Nếu user chỉ có customer role:** ở Public Area (xem dịch vụ, đặt lịch như khách hàng bình thường)
   - Không có role switcher UI (simpler approach)

4. ✅ **Role Assignment:** Admin gán role thủ công, không cần approval workflow, có hiệu lực ngay lập tức

5. ✅ **Medical Notes Security:** Database encryption at rest (Supabase default), không cần app-level encryption

6. ✅ **Audit Log Retention:** Unified policy 1 năm cho tất cả events

7. ✅ **Payment Permissions:** Technician KHÔNG xem payment history, Admin có quyền refund (ghi nhận hệ thống)

**Câu hỏi kỹ thuật chưa giải quyết:**

1. ❓ **JWT Public Key:** Lấy từ Supabase URL nào? Có cần refresh key không?
2. ❓ **Webhook Security:** Supabase webhook gọi backend như thế nào? Cần verify signature không?
3. ❓ **Token Refresh:** Backend có cần endpoint refresh token hay để frontend xử lý?
4. ❓ **Session Management:** Có cần lưu sessions trong Redis không?

**Vấn đề cần đầu vào từ bên liên quan:**

- **DevOps:** Redis configuration cho production (cluster/standalone?)
- **Frontend Team:**
  - JWT được lưu ở đâu? (localStorage/cookie?)
  - Role switcher UI design như thế nào?
  - Primary role được xác định bằng cách nào? (order in user_roles table hoặc explicit flag?)

**Nghiên cứu cần thiết:**

- [ ] Tìm hiểu Supabase webhook payload format
- [ ] Research PyJWT best practices cho production
- [ ] Review Supabase RLS policies cho user_roles table (receptionist/technician access patterns)
- [ ] Benchmark JWT verification performance với/không cache
- [ ] Research medical notes encryption best practices (HIPAA/GDPR compliance)
