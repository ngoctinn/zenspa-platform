// Shared types between Frontend and Backend
// These should match the Pydantic schemas in backend

export interface UserProfile {
  id: string;
  email: string | null;
  full_name: string | null;
  phone: string | null;
  birth_date: string | null; // ISO date string
  avatar_url: string | null;
  roles: string[];
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
}

export interface UpdateUserProfileData {
  full_name?: string | null;
  phone?: string | null;
  birth_date?: string | null; // ISO date string
  avatar_url?: string | null;
}

export interface InviteStaffRequest {
  email: string;
  role: "customer" | "receptionist" | "technician" | "admin";
}

export interface UpdateRoleRequest {
  role: "customer" | "receptionist" | "technician" | "admin";
}
