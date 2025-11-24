---
phase: implementation
title: Hướng Dẫn Triển Khai - Admin User Management
description: Hướng dẫn chi tiết triển khai code, best practices và ghi chú kỹ thuật cho tính năng quản lý tài khoản người dùng
---

# Hướng Dẫn Triển Khai - Admin User Management

## Tổng Quan Triển Khai

**Code sẽ được tổ chức như thế nào?**

- **Backend:** Extend existing user module với admin routes
- **Frontend:** New admin components trong `/admin` route group
- **Database:** Use existing schema, add admin-specific queries
- **Auth:** Leverage existing Supabase JWT với admin role check

## Backend Implementation

### 1. Extend User Schemas

**File:** `backend/app/modules/user/user_schemas.py`

```python
# Thêm vào cuối file
class AdminUserProfile(SQLModel):
    """Schema cho admin xem thông tin user"""
    id: str
    email: str
    full_name: str
    phone: str | None = None
    avatar_url: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    roles: list[RoleRead] = []
    last_login: datetime | None = None

class AdminCreateUser(SQLModel):
    """Schema tạo user mới bởi admin"""
    email: str = Field(..., description="Email đăng nhập")
    full_name: str = Field(..., description="Họ tên đầy đủ")
    phone: str | None = None
    roles: list[str] = Field(default_factory=list, description="Danh sách role IDs")

class AdminUpdateUser(SQLModel):
    """Schema cập nhật user bởi admin"""
    full_name: str | None = None
    phone: str | None = None
    is_active: bool | None = None
    roles: list[str] | None = None
```

### 2. Extend User Service

**File:** `backend/app/modules/user/user_service.py`

```python
# Thêm vào cuối file
class UserAdminService:
    """Service cho admin quản lý users"""

    @staticmethod
    async def list_users(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        is_active: bool | None = None,
        role_id: str | None = None
    ) -> list[AdminUserProfile]:
        """Liệt kê users với filter"""
        query = select(UserProfile).options(
            selectinload(UserProfile.roles)
        )

        if search:
            query = query.where(
                or_(
                    UserProfile.email.ilike(f"%{search}%"),
                    UserProfile.full_name.ilike(f"%{search}%")
                )
            )

        if is_active is not None:
            query = query.where(UserProfile.is_active == is_active)

        if role_id:
            query = query.where(
                UserProfile.roles.any(Role.id == role_id)
            )

        result = await session.exec(query.offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def create_user_by_admin(
        session: AsyncSession,
        user_data: AdminCreateUser,
        admin_id: str
    ) -> UserProfile:
        """Tạo user mới bởi admin"""
        # Tạo user trong Supabase Auth (placeholder)
        # supabase_admin = get_supabase_admin_client()
        # auth_user = supabase_admin.auth.admin.create_user({...})

        # Tạo profile trong database
        profile = UserProfile(
            id=auth_user.id,  # từ Supabase
            email=user_data.email,
            full_name=user_data.full_name,
            phone=user_data.phone,
            is_active=True
        )

        session.add(profile)
        await session.commit()
        await session.refresh(profile)

        # Gán roles
        if user_data.roles:
            await UserAdminService.assign_roles_to_user(
                session, profile.id, user_data.roles
            )

        return profile

    @staticmethod
    async def assign_roles_to_user(
        session: AsyncSession,
        user_id: str,
        role_ids: list[str]
    ) -> None:
        """Gán roles cho user"""
        # Xóa roles cũ
        await session.exec(
            delete(UserRoleLink).where(UserRoleLink.user_id == user_id)
        )

        # Thêm roles mới
        for role_id in role_ids:
            link = UserRoleLink(user_id=user_id, role_id=role_id)
            session.add(link)

        await session.commit()
```

### 3. Admin Routes

**File:** `backend/app/modules/user/user_routes.py`

```python
# Thêm vào cuối file
@router.get("/admin/users", response_model=list[AdminUserProfile])
async def list_users_for_admin(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(require_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    search: str | None = None,
    is_active: bool | None = None,
    role_id: str | None = None
):
    """API cho admin xem danh sách users"""
    return await UserAdminService.list_users(
        session, skip, limit, search, is_active, role_id
    )

@router.post("/admin/users", response_model=AdminUserProfile)
async def create_user_by_admin(
    user_data: AdminCreateUser,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(require_admin)
):
    """API tạo user mới bởi admin"""
    return await UserAdminService.create_user_by_admin(
        session, user_data, current_user["sub"]
    )

@router.put("/admin/users/{user_id}", response_model=AdminUserProfile)
async def update_user_by_admin(
    user_id: str,
    user_data: AdminUpdateUser,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(require_admin)
):
    """API cập nhật user bởi admin"""
    # Implementation here
    pass

@router.delete("/admin/users/{user_id}")
async def delete_user_by_admin(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(require_admin)
):
    """API xóa user bởi admin (soft delete)"""
    # Implementation here
    pass
```

## Frontend Implementation

### 1. API Client

**File:** `frontend/apiRequests/adminUser.ts`

```typescript
import { apiRequest } from "@/lib/utils";

export interface AdminUserProfile {
  id: string;
  email: string;
  full_name: string;
  phone: string | null;
  avatar_url: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  roles: Role[];
  last_login: string | null;
}

export interface CreateUserRequest {
  email: string;
  full_name: string;
  phone?: string;
  roles: string[];
}

export const adminUserApi = {
  async listUsers(params?: {
    skip?: number;
    limit?: number;
    search?: string;
    is_active?: boolean;
    role_id?: string;
  }) {
    return apiRequest<AdminUserProfile[]>("/admin/users", {
      method: "GET",
      params,
    });
  },

  async createUser(data: CreateUserRequest) {
    return apiRequest<AdminUserProfile>("/admin/users", {
      method: "POST",
      body: data,
    });
  },

  async updateUser(userId: string, data: Partial<CreateUserRequest>) {
    return apiRequest<AdminUserProfile>(`/admin/users/${userId}`, {
      method: "PUT",
      body: data,
    });
  },

  async deleteUser(userId: string) {
    return apiRequest(`/admin/users/${userId}`, {
      method: "DELETE",
    });
  },
};
```

### 2. Main Page Component

**File:** `frontend/app/admin/users/page.tsx`

```typescript
"use client";

import { useState, useEffect } from "react";
import { AdminUserManagementPage } from "@/components/admin/user-management-page";

export default function AdminUsersPage() {
  return <AdminUserManagementPage />;
}
```

### 3. Main Component

**File:** `frontend/components/admin/user-management-page.tsx`

```typescript
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { UserListTable } from "./user-list-table";
import { UserCreateDialog } from "./user-create-dialog";
import { adminUserApi, AdminUserProfile } from "@/apiRequests/adminUser";

export function AdminUserManagementPage() {
  const [users, setUsers] = useState<AdminUserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [createDialogOpen, setCreateDialogOpen] = useState(false);

  useEffect(() => {
    loadUsers();
  }, [search]);

  const loadUsers = async () => {
    try {
      const data = await adminUserApi.listUsers({ search });
      setUsers(data);
    } catch (error) {
      console.error("Failed to load users:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (userData: any) => {
    await adminUserApi.createUser(userData);
    setCreateDialogOpen(false);
    loadUsers();
  };

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Quản Lý Tài Khoản Người Dùng</h1>
        <Button onClick={() => setCreateDialogOpen(true)}>
          Tạo Tài Khoản Mới
        </Button>
      </div>

      <div className="mb-4">
        <Input
          placeholder="Tìm kiếm theo email hoặc tên..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="max-w-sm"
        />
      </div>

      <UserListTable users={users} loading={loading} onRefresh={loadUsers} />

      <UserCreateDialog
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
        onSubmit={handleCreateUser}
      />
    </div>
  );
}
```

## Best Practices & Notes

### Security

- Luôn validate admin role ở backend
- Sanitize tất cả user inputs
- Log sensitive operations
- Use HTTPS only

### Performance

- Implement pagination từ sớm
- Cache role data nếu cần
- Lazy load dialogs
- Debounce search input

### Error Handling

- Centralized error handling
- User-friendly error messages
- Retry mechanisms cho network errors
- Graceful degradation

### Testing

- Test admin authorization
- Test CRUD operations
- Test edge cases (empty data, invalid inputs)
- E2E tests cho critical flows

## Deployment Checklist

- [ ] Database migrations applied
- [ ] Environment variables configured
- [ ] Admin role exists in system
- [ ] API endpoints tested
- [ ] Frontend builds successfully
- [ ] E2E tests pass
- [ ] Documentation updated
