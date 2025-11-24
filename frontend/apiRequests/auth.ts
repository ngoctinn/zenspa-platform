import { createSupabaseBrowserClient } from "@/utils/supabaseClient";
import { User } from "@supabase/supabase-js";

/**
 * Lấy thông tin người dùng hiện tại từ Supabase
 * @returns Promise<User | null>
 */
export const getCurrentUser = async (): Promise<User | null> => {
  const supabase = createSupabaseBrowserClient();
  const { data, error } = await supabase.auth.getUser();

  if (error) {
    // Nếu lỗi là do không có session (người dùng chưa đăng nhập), trả về null thay vì throw error
    if (
      error.message === "Auth session missing!" ||
      error.message.includes("Auth session missing")
    ) {
      return null;
    }
    throw new Error(`Failed to get current user: ${error.message}`);
  }
  return data.user;
};

/**
 * Đăng xuất người dùng
 * @returns Promise<void>
 */
export const signOutUser = async (): Promise<void> => {
  const supabase = createSupabaseBrowserClient();
  const { error } = await supabase.auth.signOut();
  if (error) {
    throw new Error(`Failed to sign out: ${error.message}`);
  }

  // Gọi API backend để clear session nếu cần
  try {
    await fetch("/api/auth/logout", { method: "POST" });
  } catch (error) {
    console.warn("Failed to call logout API:", error);
  }
};
