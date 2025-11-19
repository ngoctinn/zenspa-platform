# User Module

Module `user/` quản lý toàn bộ user management, authentication, roles, và profiles.

## Cấu trúc

```
user/
├── user_models.py      # SQLModel models: Profile, UserRoleLink, Role enum
├── user_schemas.py     # Pydantic schemas: ProfileBase, ProfileUpdate, UpdateRoleRequest, InviteStaffRequest
├── user_service.py     # Business logic: CRUD profiles, role management, staff invites
└── user_routes.py      # API routes: user endpoints & admin endpoints
```

## API Endpoints

### User Endpoints (`/api/v1/users`)

- `GET /me` - Lấy profile của user hiện tại
- `PUT /me` - Cập nhật profile của user hiện tại

### Admin Endpoints (`/api/v1/admin`)

- `PUT /users/{user_id}/role` - Gán role cho user (chỉ admin)
- `POST /invite-staff` - Mời staff qua email (chỉ admin)

## Models

### Profile

Bảng `profiles` - Thông tin cá nhân của user

- id (UUID, PK)
- email
- full_name
- phone
- birth_date
- avatar_url
- role (legacy field cho Supabase compatibility)
- created_at, updated_at

### UserRoleLink

Bảng `user_role_links` - Quan hệ nhiều-nhiều giữa user và role

- user_id (UUID, PK)
- role_name (Role enum, PK)
- created_at, updated_at

### Role (Enum)

- CUSTOMER = "customer"
- RECEPTIONIST = "receptionist"
- TECHNICIAN = "technician"
- ADMIN = "admin"

## Refactoring History

**Nov 17, 2025**: Consolidated `admin/` và `customer/` modules thành `user/` module duy nhất.

- Lý do: Admin và customer modules chỉ chứa user management logic, chưa có business logic riêng biệt
- Các module domain-specific (appointments, services, etc.) sẽ được tạo khi cần thiết
- Cấu trúc tương lai:
  - `user/` - User management, auth, roles, profiles
  - `customer/` - Appointments, customer history (sẽ implement)
  - `staff/` - Staff schedules, performance (sẽ implement)
  - `appointment/` - Booking logic (sẽ implement)
