import { supabase } from "@/utils/supabaseClient";

export interface UserProfile {
  id: string;
  email: string;
  full_name: string | null;
  phone: string | null;
  birth_date: string | null; // ISO date string
  avatar_url: string | null;
  role: string;
  created_at: string;
  updated_at: string;
}

export interface UpdateUserProfileData {
  full_name?: string | null;
  phone?: string | null;
  birth_date?: string | null;
  avatar_url?: string | null;
}

export const getUserProfile = async (): Promise<UserProfile> => {
  const { data: sessionData } = await supabase.auth.getSession();
  if (!sessionData.session?.access_token) {
    throw new Error("No access token");
  }

  const response = await fetch("http://localhost:8000/api/v1/users/me", {
    headers: {
      Authorization: `Bearer ${sessionData.session.access_token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch user profile");
  }

  return response.json();
};

export const updateUserProfile = async (
  data: UpdateUserProfileData
): Promise<UserProfile> => {
  const { data: sessionData } = await supabase.auth.getSession();
  if (!sessionData.session?.access_token) {
    throw new Error("No access token");
  }

  const response = await fetch("http://localhost:8000/api/v1/users/me", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${sessionData.session.access_token}`,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Failed to update user profile");
  }

  return response.json();
};
