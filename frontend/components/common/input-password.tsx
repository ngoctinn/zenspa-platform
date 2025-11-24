"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { EyeIcon, EyeOffIcon, LockIcon } from "lucide-react";
import { forwardRef, useState } from "react";

const InputPassword = forwardRef<
  HTMLInputElement,
  Omit<React.InputHTMLAttributes<HTMLInputElement>, "type">
>(({ className, ...props }, ref) => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div className="relative">
      <div className="text-muted-foreground pointer-events-none absolute inset-y-0 left-0 flex items-center justify-center pl-3 peer-disabled:opacity-50">
        <LockIcon className="size-4" />
      </div>
      <Input
        ref={ref}
        type={isVisible ? "text" : "password"}
        className={cn("pl-9 pr-9", className)}
        {...props}
      />
      <Button
        type="button"
        variant="ghost"
        onClick={() => setIsVisible((prevState) => !prevState)}
        className="text-muted-foreground focus-visible:ring-ring/50 absolute inset-y-0 right-0 h-full w-10 rounded-l-none hover:bg-transparent"
        aria-pressed={isVisible}
        aria-label={isVisible ? "Ẩn mật khẩu" : "Hiện mật khẩu"}
      >
        {isVisible ? (
          <EyeOffIcon className="size-4" />
        ) : (
          <EyeIcon className="size-4" />
        )}
      </Button>
    </div>
  );
});

InputPassword.displayName = "InputPassword";

export { InputPassword };
