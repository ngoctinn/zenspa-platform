"use client";

import {
  adminUserApi,
  AdminUserProfile,
  CreateUserRequest,
  Role,
  UpdateUserRequest,
} from "@/apiRequests/adminUser";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Plus, RefreshCcw, Search, Settings2 } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { toast } from "sonner";
import { RoleAssignmentDialog } from "./role-assignment-dialog";
import { UserCreateDialog } from "./user-create-dialog";
import { UserEditDialog } from "./user-edit-dialog";
import { UserListTable, UserTableColumnVisibility } from "./user-list-table";

export function AdminUserManagementPage() {
  const [users, setUsers] = useState<AdminUserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState<string>("all");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [visibleColumns, setVisibleColumns] =
    useState<UserTableColumnVisibility>({
      fullName: true,
      email: true,
      phone: true,
      status: true,
      roles: true,
      createdAt: true,
    });

  // Dialog states
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [roleDialogOpen, setRoleDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<AdminUserProfile | null>(
    null
  );

  // Mock roles for now
  const [availableRoles] = useState<Role[]>([
    {
      id: "admin",
      name: "Admin",
      description: "Quản trị viên hệ thống",
      permissions: [],
    },
    {
      id: "receptionist",
      name: "Receptionist",
      description: "Lễ tân",
      permissions: [],
    },
    {
      id: "technician",
      name: "Technician",
      description: "Kỹ thuật viên",
      permissions: [],
    },
    {
      id: "customer",
      name: "Customer",
      description: "Khách hàng",
      permissions: [],
    },
  ]);

  // Debounce search could be added here

  const loadUsers = useCallback(async () => {
    setLoading(true);
    try {
      // Mock data for now if API fails or returns empty
      // const data = await adminUserApi.listUsers({ search, role_id: roleFilter !== 'all' ? roleFilter : undefined, skip: (page - 1) * 10, limit: 10 })
      // setUsers(data)

      // Using mock data for UI development
      const mockUsers: AdminUserProfile[] = [
        {
          id: "1",
          email: "admin@zenspa.com",
          full_name: "Admin User",
          phone: "0901234567",
          avatar_url: null,
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          roles: [
            {
              id: "admin",
              name: "Admin",
              description: "Administrator",
              permissions: [],
            },
          ],
          last_login: new Date().toISOString(),
        },
        {
          id: "2",
          email: "staff@zenspa.com",
          full_name: "Staff User",
          phone: "0901234568",
          avatar_url: null,
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          roles: [
            {
              id: "receptionist",
              name: "Receptionist",
              description: "Lễ tân",
              permissions: [],
            },
          ],
          last_login: new Date().toISOString(),
        },
        {
          id: "3",
          email: "tech@zenspa.com",
          full_name: "Technician User",
          phone: "0901234569",
          avatar_url: null,
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          roles: [
            {
              id: "technician",
              name: "Technician",
              description: "Kỹ thuật viên",
              permissions: [],
            },
          ],
          last_login: new Date().toISOString(),
        },
        {
          id: "4",
          email: "customer@zenspa.com",
          full_name: "Customer User",
          phone: "0901234570",
          avatar_url: null,
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          roles: [
            {
              id: "customer",
              name: "Customer",
              description: "Khách hàng",
              permissions: [],
            },
          ],
          last_login: new Date().toISOString(),
        },
        {
          id: "5",
          email: "manager@zenspa.com",
          full_name: "Manager User",
          phone: "0901234571",
          avatar_url: null,
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          roles: [
            {
              id: "admin",
              name: "Admin",
              description: "Administrator",
              permissions: [],
            },
            {
              id: "receptionist",
              name: "Receptionist",
              description: "Lễ tân",
              permissions: [],
            },
          ],
          last_login: new Date().toISOString(),
        },
      ];

      // Filter mock data
      let filtered = mockUsers.filter(
        (u) =>
          u.email.toLowerCase().includes(search.toLowerCase()) ||
          u.full_name.toLowerCase().includes(search.toLowerCase())
      );

      if (roleFilter !== "all") {
        filtered = filtered.filter((u) =>
          u.roles.some((r) => r.id === roleFilter)
        );
      }

      // Mock pagination
      const pageSize = 10;
      setTotalPages(Math.ceil(filtered.length / pageSize) || 1);
      const paginated = filtered.slice((page - 1) * pageSize, page * pageSize);

      setUsers(paginated);
    } catch (error) {
      console.error("Failed to load users:", error);
      toast.error("Không thể tải danh sách người dùng");
    } finally {
      setLoading(false);
    }
  }, [search, roleFilter, page]);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  const handleCreateUser = async (data: CreateUserRequest) => {
    try {
      await adminUserApi.createUser(data);
      toast.success("Tạo tài khoản thành công");
      loadUsers();
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Tạo tài khoản thất bại";
      toast.error(message);
      // For mock demo, just add to list
      console.log("Mock create:", data);
    }
  };

  const handleUpdateUser = async (userId: string, data: UpdateUserRequest) => {
    try {
      await adminUserApi.updateUser(userId, data);
      toast.success("Cập nhật tài khoản thành công");
      loadUsers();
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Cập nhật thất bại";
      toast.error(message);
      console.log("Mock update:", userId, data);
    }
  };

  const handleAssignRoles = async (userId: string, roleIds: string[]) => {
    try {
      // This endpoint might need to be added to API client
      // await adminUserApi.assignRoles(userId, roleIds)
      toast.success("Phân quyền thành công");
      loadUsers();
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Phân quyền thất bại";
      toast.error(message);
      console.log("Mock assign roles:", userId, roleIds);
    }
  };

  const handleDeleteUser = async (user: AdminUserProfile) => {
    if (!confirm(`Bạn có chắc chắn muốn xóa tài khoản ${user.email}?`)) return;

    try {
      await adminUserApi.deleteUser(user.id);
      toast.success("Xóa tài khoản thành công");
      loadUsers();
    } catch (error) {
      const message = error instanceof Error ? error.message : "Xóa thất bại";
      toast.error(message);
      console.log("Mock delete:", user.id);
    }
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div className="flex flex-1 items-center space-x-2 w-full md:w-auto">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Tìm kiếm theo email hoặc tên..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-8"
            />
          </div>
          <Select value={roleFilter} onValueChange={setRoleFilter}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Lọc theo vai trò" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Tất cả vai trò</SelectItem>
              {availableRoles.map((role) => (
                <SelectItem key={role.id} value={role.id}>
                  {role.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={loadUsers}>
            <RefreshCcw className="mr-2 h-4 w-4" />
            Làm mới
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm">
                <Settings2 className="mr-2 h-4 w-4" />
                Cột
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Chọn cột hiển thị</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuCheckboxItem
                checked={visibleColumns.email}
                onCheckedChange={(checked) =>
                  setVisibleColumns((prev) => ({ ...prev, email: checked }))
                }
              >
                Email
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={visibleColumns.fullName}
                onCheckedChange={(checked) =>
                  setVisibleColumns((prev) => ({ ...prev, fullName: checked }))
                }
              >
                Họ Tên
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={visibleColumns.phone}
                onCheckedChange={(checked) =>
                  setVisibleColumns((prev) => ({ ...prev, phone: checked }))
                }
              >
                Số Điện Thoại
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={visibleColumns.status}
                onCheckedChange={(checked) =>
                  setVisibleColumns((prev) => ({ ...prev, status: checked }))
                }
              >
                Trạng Thái
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={visibleColumns.roles}
                onCheckedChange={(checked) =>
                  setVisibleColumns((prev) => ({ ...prev, roles: checked }))
                }
              >
                Vai Trò
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={visibleColumns.createdAt}
                onCheckedChange={(checked) =>
                  setVisibleColumns((prev) => ({ ...prev, createdAt: checked }))
                }
              >
                Ngày Tạo
              </DropdownMenuCheckboxItem>
            </DropdownMenuContent>
          </DropdownMenu>
          <Button onClick={() => setCreateDialogOpen(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Tạo Tài Khoản
          </Button>
        </div>
      </div>

      <UserListTable
        users={users}
        loading={loading}
        visibleColumns={visibleColumns}
        page={page}
        totalPages={totalPages}
        onPageChange={setPage}
        onEdit={(user) => {
          setSelectedUser(user);
          setEditDialogOpen(true);
        }}
        onAssignRole={(user) => {
          setSelectedUser(user);
          setRoleDialogOpen(true);
        }}
        onDelete={handleDeleteUser}
      />

      <UserCreateDialog
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
        onSubmit={handleCreateUser}
      />

      <UserEditDialog
        user={selectedUser}
        open={editDialogOpen}
        onOpenChange={setEditDialogOpen}
        onSubmit={handleUpdateUser}
      />

      <RoleAssignmentDialog
        user={selectedUser}
        open={roleDialogOpen}
        onOpenChange={setRoleDialogOpen}
        onSubmit={handleAssignRoles}
        availableRoles={availableRoles}
      />
    </div>
  );
}
