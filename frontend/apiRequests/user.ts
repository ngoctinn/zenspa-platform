import { supabase } from "@/utils/supabaseClient";

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  role: string;
}

export const getUserProfile = async (): Promise<UserProfile> => {
  const { data: sessionData } = await supabase.auth.getSession();
  if (!sessionData.session?.access_token) {
    throw new Error("No access token");
  }

  const response = await fetch("/api/v1/users/me", {
    headers: {
      Authorization: `Bearer ${sessionData.session.access_token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch user profile");
  }

  return response.json();
};
