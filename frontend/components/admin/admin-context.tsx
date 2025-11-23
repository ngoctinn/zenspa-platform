"use client";

import { getUserProfile, UserProfile } from "@/apiRequests/user";
import { createContext, useContext, useEffect, useState } from "react";

interface AdminContextType {
  user: UserProfile | null;
  isSidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  isLoading: boolean;
}

const AdminContext = createContext<AdminContextType | undefined>(undefined);

export function AdminProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load sidebar state
    const savedState = localStorage.getItem("sidebarOpen");
    if (savedState !== null) {
      setIsSidebarOpen(savedState === "true");
    }

    // Fetch user
    const fetchUser = async () => {
      try {
        const profile = await getUserProfile();
        setUser(profile);
      } catch (error) {
        console.error("Failed to fetch user profile", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchUser();
  }, []);

  const setSidebarOpen = (open: boolean) => {
    setIsSidebarOpen(open);
    localStorage.setItem("sidebarOpen", String(open));
  };

  return (
    <AdminContext.Provider
      value={{ user, isSidebarOpen, setSidebarOpen, isLoading }}
    >
      {children}
    </AdminContext.Provider>
  );
}

export const useAdmin = () => {
  const context = useContext(AdminContext);
  if (!context) throw new Error("useAdmin must be used within AdminProvider");
  return context;
};
