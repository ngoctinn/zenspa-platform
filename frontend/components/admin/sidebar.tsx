"use client";

import Link from "next/link";

import { Menu } from "@/components/admin/menu";
import { SidebarToggle } from "@/components/admin/sidebar-toggle";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: () => void;
  userRoles?: string[];
}

export function Sidebar({ isOpen, setIsOpen, userRoles }: SidebarProps) {
  return (
    <aside
      className={cn(
        "fixed top-0 left-0 z-20 h-screen -translate-x-full lg:translate-x-0 transition-[width] ease-in-out duration-300",
        !isOpen ? "w-[90px]" : "w-72"
      )}
    >
      <SidebarToggle isOpen={isOpen} setIsOpen={setIsOpen} />
      <div className="relative h-full flex flex-col px-3 py-4 overflow-y-auto shadow-md dark:shadow-zinc-800">
        <Button
          className={cn(
            "transition-all ease-in-out duration-300 mb-1",
            !isOpen ? "translate-x-1" : "translate-x-0"
          )}
          variant="link"
          asChild
        >
          <Link href="/admin/dashboard" className="flex items-center gap-2">
            <h1
              className={cn(
                "font-bold text-lg whitespace-nowrap transition-all ease-in-out duration-300",
                !isOpen
                  ? "-translate-x-8 opacity-0 scale-75"
                  : "translate-x-0 opacity-100 scale-100"
              )}
            >
              ZENSPA
            </h1>
          </Link>
        </Button>
        <Menu isOpen={isOpen} userRoles={userRoles} />
      </div>
    </aside>
  );
}
