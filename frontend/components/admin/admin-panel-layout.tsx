"use client";

import { AdminProvider, useAdmin } from "@/components/admin/admin-context";
import { Footer } from "@/components/admin/footer";
import { Sidebar } from "@/components/admin/sidebar";
import { cn } from "@/lib/utils";

function AdminPanelInner({ children }: { children: React.ReactNode }) {
  const { isSidebarOpen, setSidebarOpen, user } = useAdmin();

  return (
    <>
      <Sidebar
        isOpen={isSidebarOpen}
        setIsOpen={() => setSidebarOpen(!isSidebarOpen)}
        userRoles={user?.roles}
      />
      <main
        className={cn(
          "min-h-[calc(100vh_-_56px)] bg-zinc-50 dark:bg-zinc-900 transition-[margin-left] ease-in-out duration-300",
          !isSidebarOpen ? "lg:ml-[90px]" : "lg:ml-72"
        )}
      >
        {children}
      </main>
      <footer
        className={cn(
          "transition-[margin-left] ease-in-out duration-300",
          !isSidebarOpen ? "lg:ml-[90px]" : "lg:ml-72"
        )}
      >
        <Footer />
      </footer>
    </>
  );
}

export default function AdminPanelLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AdminProvider>
      <AdminPanelInner>{children}</AdminPanelInner>
    </AdminProvider>
  );
}
