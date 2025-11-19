# Refactoring: Consolidate Admin & Customer → User Module

**Date**: November 17, 2025
**Status**: ✅ Completed

## Lý do Refactor

Trước refactor, cấu trúc module không hợp lý:

- `admin/` module: Chỉ có invite staff & assign roles → User management
- `customer/` module: Chỉ có Profile model & get profile → Cũng là user info
- Chưa có customer-specific features (appointments, services, notifications)

Theo quy tắc trong `overview.instructions.md`, modules nên theo domain thực tế (appointment, staff, customer business logic), không phải theo role.

## Thay đổi

### Trước

```
modules/
├── admin/
│   ├── admin_models.py    # UserRoleLink, Role
│   ├── admin_schemas.py   # UpdateRoleRequest, InviteStaffRequest
│   ├── admin_service.py   # update_user_role, invite_staff
│   └── admin_routes.py    # Admin endpoints
└── customer/
    ├── customer_models.py # Profile
    ├── customer_schemas.py# ProfileBase, ProfileUpdate
    ├── customer_service.py# get_profile, update_profile
    └── customer_routes.py # User endpoints
```

### Sau

```
modules/
└── user/
    ├── user_models.py     # Profile, UserRoleLink, Role (consolidated)
    ├── user_schemas.py    # All user-related schemas
    ├── user_service.py    # Profile CRUD + role management + invites
    ├── user_routes.py     # router (user endpoints) + admin_router (admin endpoints)
    └── README.md          # Documentation
```

## Files Modified

### Created

- ✅ `app/modules/user/README.md` - Module documentation
- ✅ `tests/test_user.py` - Consolidated tests

### Updated

- ✅ `app/modules/user/user_routes.py` - Added admin_router, consolidated routes
- ✅ `app/api/api_v1.py` - Import từ user module
- ✅ `app/api/admin.py` - Re-export admin_router từ user module
- ✅ `app/api/users.py` - Re-export router từ user module
- ✅ `alembic/env.py` - Import models từ user module

### Deleted

- 🗑️ `app/modules/admin/` - Entire directory
- 🗑️ `app/modules/customer/` - Entire directory
- 🗑️ `tests/test_admin.py` - Replaced by test_user.py

## API Endpoints (Unchanged)

User endpoints vẫn giữ nguyên:

- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile

Admin endpoints vẫn giữ nguyên:

- `PUT /api/v1/admin/users/{user_id}/role` - Assign role (admin only)
- `POST /api/v1/admin/invite-staff` - Invite staff (admin only)

## Testing Results

```bash
# Test user module
pytest tests/test_user.py -v
# Result: ✅ 6/6 passed

# Test full suite
pytest tests/ -v
# Result: ✅ 24/30 passed (6 failures pre-existing, not related to refactor)
```

## Server Status

✅ Server starts successfully
✅ No import errors
✅ API documentation accessible at `/docs`

## Cấu trúc Tương Lai

Khi implement business logic thực tế, sẽ tạo thêm:

- `customer/` - Appointments, customer history, loyalty points
- `staff/` - Staff schedules, performance tracking
- `appointment/` - Booking logic, service management
- `notification/` - Real-time notifications, email

Module `user/` sẽ chỉ chứa user management (auth, roles, profiles).

## Notes

- Module duplication đã được loại bỏ
- Code structure rõ ràng hơn, dễ maintain
- Tuân thủ quy tắc domain-driven design trong overview.instructions.md
- Không ảnh hưởng đến API contracts hoặc database schema
