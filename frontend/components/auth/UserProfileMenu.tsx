import { CalendarIcon, LogOutIcon, UserIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator, // 1. Import thêm Separator
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { User } from "@supabase/supabase-js";

interface UserProfileMenuProps {
  user: User;
  onLogout?: () => void;
}

// Bạn không cần 'listItems' nữa nếu dùng cách này
// const listItems = [ ... ];

export const UserProfileMenu = ({ user, onLogout }: UserProfileMenuProps) => {
  const displayName =
    user.user_metadata?.name || user.email?.split("@")[0] || "User";
  const avatarUrl = user.user_metadata?.avatar_url;

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="secondary"
          size="icon"
          className="overflow-hidden rounded-full"
        >
          <img
            src={
              avatarUrl ||
              "https://cdn.shadcnstudio.com/ss-assets/avatar/avatar-5.png"
            }
            alt={displayName}
          />
        </Button>
      </DropdownMenuTrigger>

      {/* 2. Thêm sideOffset để menu không dính sát nút avatar */}
      <DropdownMenuContent className="w-56" align="end" sideOffset={8}>
        {/* 3. Cá nhân hóa lời chào */}
        <DropdownMenuLabel>Chào, {displayName}</DropdownMenuLabel>
        <DropdownMenuSeparator />

        <DropdownMenuGroup>
          {/* 4. Đây là cách chuẩn để thêm icon trong Shadcn */}
          <DropdownMenuItem>
            <UserIcon className="mr-2 h-4 w-4" />
            <span>Hồ sơ</span>
          </DropdownMenuItem>
          <DropdownMenuItem>
            <CalendarIcon className="mr-2 h-4 w-4" />
            <span>Lịch hẹn của tôi</span>
          </DropdownMenuItem>
        </DropdownMenuGroup>

        <DropdownMenuSeparator />

        {/* 5. Tạo kiểu "nguy hiểm" (destructive) cho nút Đăng xuất */}
        <DropdownMenuItem
          onClick={onLogout}
          className="text-red-500 focus:text-red-500 focus:bg-red-50"
        >
          <LogOutIcon className="mr-2 h-4 w-4" />
          <span>Đăng xuất</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
