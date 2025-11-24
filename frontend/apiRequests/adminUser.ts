import { http } from "@/lib/http";

export interface Role {
  id: string;
  name: string;
  description: string;
  permissions: string[];
}

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

export interface UpdateUserRequest {
  full_name?: string;
  phone?: string;
  is_active?: boolean;
  roles?: string[];
}

export const adminUserApi = {
  async listUsers(params?: {
    skip?: number;
    limit?: number;
    search?: string;
    is_active?: boolean;
    role_id?: string;
  }) {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, String(value));
        }
      });
    }
    const queryString = searchParams.toString();
    const url = queryString ? `/admin/users?${queryString}` : "/admin/users";

    return http.get<AdminUserProfile[]>(url);
  },

  async createUser(data: CreateUserRequest) {
    return http.post<AdminUserProfile>("/admin/users", data);
  },

  async updateUser(userId: string, data: Partial<UpdateUserRequest>) {
    return http.put<AdminUserProfile>(`/admin/users/${userId}`, data);
  },

  async deleteUser(userId: string) {
    return http.delete(`/admin/users/${userId}`);
  },

  async listRoles() {
    // Mock implementation or real endpoint if available
    // return http.get<Role[]>('/admin/roles')
    return [] as Role[];
  },
};
