import {
  Calendar,
  LayoutGrid,
  LucideIcon,
  Package,
  Settings,
  Tag,
  UserCog,
  Users,
} from "lucide-react";

type Submenu = {
  href: string;
  label: string;
  active?: boolean;
  roles?: string[]; // Roles that can see this submenu
};

type Menu = {
  href: string;
  label: string;
  active?: boolean;
  icon: LucideIcon;
  submenus?: Submenu[];
  roles?: string[]; // Roles that can see this menu
};

type Group = {
  groupLabel: string;
  menus: Menu[];
};

export function getMenuList(pathname: string): Group[] {
  return [
    {
      groupLabel: "",
      menus: [
        {
          href: "/admin/dashboard",
          label: "Tổng quan",
          active: pathname.includes("/admin/dashboard"),
          icon: LayoutGrid,
          submenus: [],
          roles: ["admin", "receptionist", "technician"],
        },
      ],
    },
    {
      groupLabel: "Quản lý",
      menus: [
        {
          href: "/admin/appointments",
          label: "Lịch hẹn",
          active: pathname.includes("/admin/appointments"),
          icon: Calendar,
          roles: ["admin", "receptionist"],
        },
        {
          href: "/admin/customers",
          label: "Khách hàng",
          active: pathname.includes("/admin/customers"),
          icon: Users,
          roles: ["admin", "receptionist"],
        },
        {
          href: "/admin/staff",
          label: "Nhân viên",
          active: pathname.includes("/admin/staff"),
          icon: UserCog,
          roles: ["admin"],
        },
        {
          href: "/admin/services",
          label: "Dịch vụ",
          active: pathname.includes("/admin/services"),
          icon: Tag,
          roles: ["admin"],
        },
        {
          href: "/admin/products",
          label: "Sản phẩm",
          active: pathname.includes("/admin/products"),
          icon: Package,
          roles: ["admin", "receptionist"],
        },
      ],
    },
    {
      groupLabel: "Cài đặt",
      menus: [
        {
          href: "/admin/users",
          label: "Người dùng",
          active: pathname.includes("/admin/users"),
          icon: Users,
          roles: ["admin"],
        },
        {
          href: "/admin/settings",
          label: "Cấu hình",
          active: pathname.includes("/admin/settings"),
          icon: Settings,
          roles: ["admin"],
        },
      ],
    },
  ];
}
