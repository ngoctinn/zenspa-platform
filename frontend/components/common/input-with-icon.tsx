import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { UserIcon } from "lucide-react";
import { forwardRef } from "react";

interface InputWithIconProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  icon?: React.ReactNode;
}

const InputWithIcon = forwardRef<HTMLInputElement, InputWithIconProps>(
  ({ className, icon = <UserIcon className="size-4" />, ...props }, ref) => {
    return (
      <div className="relative">
        <div className="text-muted-foreground pointer-events-none absolute inset-y-0 left-0 flex items-center justify-center pl-3 peer-disabled:opacity-50">
          {icon}
        </div>
        <Input ref={ref} className={cn("peer pl-9", className)} {...props} />
      </div>
    );
  }
);

InputWithIcon.displayName = "InputWithIcon";

export { InputWithIcon };
