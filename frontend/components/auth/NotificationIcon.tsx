import { Badge } from "@/components/ui/badge";
import { Bell } from "lucide-react";

interface NotificationIconProps {
  count: number;
}

const NotificationIcon = ({ count }: NotificationIconProps) => {
  return (
    <div className="relative">
      <Bell className="h-6 w-6 text-primary-foreground cursor-pointer" />
      {count > 0 && (
        <Badge
          variant="destructive"
          className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center p-0 text-xs"
        >
          {count > 99 ? "99+" : count}
        </Badge>
      )}
    </div>
  );
};

export default NotificationIcon;
