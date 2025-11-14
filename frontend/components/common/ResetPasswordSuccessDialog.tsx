"use client";

import { CheckCircleIcon } from "lucide-react";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface ResetPasswordSuccessDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onGoHome: () => void;
}

const ResetPasswordSuccessDialog = ({
  open,
  onOpenChange,
  onGoHome,
}: ResetPasswordSuccessDialogProps) => {
  const [timeLeft, setTimeLeft] = useState(300); // 5 phút = 300 giây

  useEffect(() => {
    if (open) {
      const timer = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            clearInterval(timer);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => {
        clearInterval(timer);
        setTimeLeft(300);
      };
    }
  }, [open]);

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader className="items-center">
          <div className="bg-[var(--success)]/10 mx-auto mb-2 flex size-12 items-center justify-center rounded-full">
            <CheckCircleIcon className="text-[var(--success)] size-6" />
          </div>
          <DialogTitle>Email đã được gửi!</DialogTitle>
          <DialogDescription className="text-center">
            Email đặt lại mật khẩu đã được gửi. Vui lòng kiểm tra hộp thư và
            click vào link để đặt mật khẩu mới.
          </DialogDescription>
        </DialogHeader>

        <div className="text-center text-sm text-muted-foreground">
          Lưu ý: Link sẽ hết hạn sau 1 giờ.
        </div>

        <DialogFooter className="flex-col-reverse gap-2 sm:flex-row sm:justify-center">
          <Button disabled variant="default">
            Thời gian còn lại: {formatTime(timeLeft)}
          </Button>
          <Button variant="outline" onClick={onGoHome}>
            Quay về trang chủ
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export { ResetPasswordSuccessDialog };
