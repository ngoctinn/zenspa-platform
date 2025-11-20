"use client";

import {
  BellIcon,
  CalendarIcon,
  LogOutIcon,
  PackageIcon,
  UserIcon,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import { getUserProfile } from "@/apiRequests/user";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { User } from "@supabase/supabase-js";

interface UserProfileMenuProps {
  user: User;
  onLogout?: () => void;
}

interface UserProfileMenuProps {
  user: User;
  onLogout?: () => void;
}

interface Profile {
  full_name: string | null;
  avatar_url: string | null;
}

// Bạn không cần 'listItems' nữa nếu dùng cách này
// const listItems = [ ... ];

export const UserProfileMenu = ({ user, onLogout }: UserProfileMenuProps) => {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const data = await getUserProfile();
        setProfile(data);
      } catch (error) {
        console.error("Failed to load profile:", error);
      } finally {
        setLoading(false);
      }
    };
    loadProfile();
  }, []);

  const fullname = loading
    ? "Loading..."
    : profile?.full_name || user.user_metadata?.full_name || "User";
  const email = user.email || "";
  const avatarUrl = profile?.avatar_url || user.user_metadata?.avatar_url;

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-10 w-10 rounded-full">
          <Avatar className="h-10 w-10">
            <AvatarImage
              src={
                avatarUrl ||
                "https://cdn.shadcnstudio.com/ss-assets/avatar/avatar-5.png"
              }
              alt={fullname}
            />
            <AvatarFallback>{fullname?.charAt(0)}</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>

      {/* 2. Thêm sideOffset để menu không dính sát nút avatar */}
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">{fullname}</p>
            <p className="text-xs leading-none text-muted-foreground">
              {email}
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem asChild>
            <Link href="/account/profile" className="cursor-pointer">
              <UserIcon className="mr-2 h-4 w-4" />
              <span>Hồ sơ</span>
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem asChild>
            <Link href="/account/appointments" className="cursor-pointer">
              <CalendarIcon className="mr-2 h-4 w-4" />
              <span>Lịch hẹn của tôi</span>
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem asChild>
            <Link href="/account/services" className="cursor-pointer">
              <PackageIcon className="mr-2 h-4 w-4" />
              <span>Liệu trình</span>
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem asChild>
            <Link href="/account/notifications" className="cursor-pointer">
              <BellIcon className="mr-2 h-4 w-4" />
              <span>Thông báo</span>
            </Link>
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          onClick={onLogout}
          className="text-red-600 focus:text-red-600 cursor-pointer"
        >
          <LogOutIcon className="mr-2 h-4 w-4" />
          <span>Đăng xuất</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
