"use client";

import { AdminUserProfile } from "@/apiRequests/adminUser";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
} from "@/components/ui/pagination";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { format } from "date-fns";
import { vi } from "date-fns/locale";
import { Edit, MoreHorizontal, Shield, Trash } from "lucide-react";

export interface UserTableColumnVisibility {
  email: boolean;
  fullName: boolean;
  phone: boolean;
  status: boolean;
  roles: boolean;
  createdAt: boolean;
}

interface UserListTableProps {
  users: AdminUserProfile[];
  loading: boolean;
  visibleColumns: UserTableColumnVisibility;
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  onEdit: (user: AdminUserProfile) => void;
  onAssignRole: (user: AdminUserProfile) => void;
  onDelete: (user: AdminUserProfile) => void;
}

export function UserListTable({
  users,
  loading,
  visibleColumns,
  page,
  totalPages,
  onPageChange,
  onEdit,
  onAssignRole,
  onDelete,
}: UserListTableProps) {
  if (loading) {
    return <div>Đang tải dữ liệu...</div>;
  }

  const visibleCount = Object.values(visibleColumns).filter(Boolean).length + 1;

  return (
    <div className="space-y-4">
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[50px]">Ảnh</TableHead>
              {visibleColumns.fullName && <TableHead>Họ Tên</TableHead>}
              {visibleColumns.email && <TableHead>Email</TableHead>}
              {visibleColumns.phone && <TableHead>Số Điện Thoại</TableHead>}
              {visibleColumns.status && <TableHead>Trạng Thái</TableHead>}
              {visibleColumns.roles && <TableHead>Vai Trò</TableHead>}
              {visibleColumns.createdAt && <TableHead>Ngày Tạo</TableHead>}
              <TableHead className="text-right">Thao Tác</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.length === 0 ? (
              <TableRow>
                <TableCell colSpan={visibleCount} className="h-24 text-center">
                  Không tìm thấy người dùng nào.
                </TableCell>
              </TableRow>
            ) : (
              users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>
                    <Avatar className="h-9 w-9">
                      <AvatarImage
                        src={user.avatar_url || ""}
                        alt={user.full_name}
                      />
                      <AvatarFallback>
                        {user.full_name.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  </TableCell>
                  {visibleColumns.fullName && (
                    <TableCell>
                      <div className="font-medium">{user.full_name}</div>
                    </TableCell>
                  )}
                  {visibleColumns.email && <TableCell>{user.email}</TableCell>}
                  {visibleColumns.phone && (
                    <TableCell>{user.phone || "-"}</TableCell>
                  )}
                  {visibleColumns.status && (
                    <TableCell>
                      <Badge variant={user.is_active ? "default" : "secondary"}>
                        {user.is_active ? "Hoạt động" : "Đã khóa"}
                      </Badge>
                    </TableCell>
                  )}
                  {visibleColumns.roles && (
                    <TableCell>
                      <div className="flex flex-wrap gap-1">
                        {user.roles.slice(0, 1).map((role) => (
                          <Badge key={role.id} variant="outline">
                            {role.name}
                          </Badge>
                        ))}
                        {user.roles.length > 1 && (
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Badge
                                  variant="outline"
                                  className="cursor-help"
                                >
                                  +{user.roles.length - 1}
                                </Badge>
                              </TooltipTrigger>
                              <TooltipContent>
                                <div className="flex flex-col gap-1">
                                  {user.roles.slice(1).map((role) => (
                                    <span key={role.id}>{role.name}</span>
                                  ))}
                                </div>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        )}
                      </div>
                    </TableCell>
                  )}
                  {visibleColumns.createdAt && (
                    <TableCell>
                      {format(new Date(user.created_at), "dd/MM/yyyy", {
                        locale: vi,
                      })}
                    </TableCell>
                  )}
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <span className="sr-only">Mở menu</span>
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Thao tác</DropdownMenuLabel>
                        <DropdownMenuItem
                          onClick={() => navigator.clipboard.writeText(user.id)}
                        >
                          Sao chép ID
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem onClick={() => onEdit(user)}>
                          <Edit className="mr-2 h-4 w-4" />
                          Chỉnh sửa
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => onAssignRole(user)}>
                          <Shield className="mr-2 h-4 w-4" />
                          Phân quyền
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem
                          className="text-red-600"
                          onClick={() => onDelete(user)}
                        >
                          <Trash className="mr-2 h-4 w-4" />
                          Xóa tài khoản
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <Pagination>
          <PaginationContent>
            <PaginationItem>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onPageChange(page - 1)}
                disabled={page <= 1}
              >
                Trước
              </Button>
            </PaginationItem>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
              <PaginationItem key={p}>
                <PaginationLink
                  isActive={page === p}
                  onClick={() => onPageChange(p)}
                >
                  {p}
                </PaginationLink>
              </PaginationItem>
            ))}
            <PaginationItem>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onPageChange(page + 1)}
                disabled={page >= totalPages}
              >
                Sau
              </Button>
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
}
