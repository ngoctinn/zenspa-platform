"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { BellIcon, CalendarIcon, PackageIcon, UserIcon } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const menuItems = [
  { href: "/account/profile", label: "Hồ sơ của tôi", icon: UserIcon },
  {
    href: "/account/appointments",
    label: "Lịch hẹn của tôi",
    icon: CalendarIcon,
  },
  { href: "/account/services", label: "Liệu trình", icon: PackageIcon },
  { href: "/account/notifications", label: "Thông báo", icon: BellIcon },
];

const SidebarMenu = () => {
  const pathname = usePathname();

  return (
    <nav className="space-y-2">
      {menuItems.map((item) => {
        const Icon = item.icon;
        const isActive = pathname === item.href;
        return (
          <Button
            key={item.href}
            variant="ghost"
            className={cn(
              "w-full justify-start gap-2",
              isActive && "text-primary border border-primary/20 bg-primary/5"
            )}
            asChild
          >
            <Link href={item.href}>
              <Icon className="size-4" />
              {item.label}
            </Link>
          </Button>
        );
      })}
    </nav>
  );
};

export default SidebarMenu;
