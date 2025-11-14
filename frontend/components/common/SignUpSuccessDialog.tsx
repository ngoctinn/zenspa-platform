"use client";

import { CheckCircleIcon } from "lucide-react";
import { useEffect, useState } from "react";

// Thay đổi 1: Nhập component từ "dialog" thay vì "alert-dialog"
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
// AlertDialogAction không còn cần thiết nữa

interface SignUpSuccessDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onGoHome: () => void;
}

const SignUpSuccessDialog = ({
  open,
  onOpenChange,
  onGoHome,
}: SignUpSuccessDialogProps) => {
  const [timeLeft, setTimeLeft] = useState(600); // 10 phút = 600 giây

  useEffect(() => {
    // Chỉ chạy logic NẾU dialog đang mở (open = true)
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

      // Hàm cleanup (dọn dẹp):
      // Sẽ được gọi khi `open` thay đổi từ `true` -> `false`
      // hoặc khi component bị unmount.
      return () => {
        clearInterval(timer);
        setTimeLeft(600); // <-- ĐẶT RESET VÀO ĐÂY
      };
    }
    // Nếu `open` là `false` ngay từ đầu, không làm gì cả.
  }, [open]);

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  };

  // Thay đổi 2: Sử dụng "Dialog" thay vì "AlertDialog"
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      {/* Thay đổi 3: Sử dụng "DialogContent" */}
      {/* DialogContent của shadcn mặc định đã có nút 'x' (DialogClose) */}
      <DialogContent className="sm:max-w-md">
        {/* Thay đổi 4: Sử dụng "DialogHeader" */}
        <DialogHeader className="items-center">
          <div className="bg-[var(--success)]/10 mx-auto mb-2 flex size-12 items-center justify-center rounded-full">
            <CheckCircleIcon className="text-[var(--success)] size-6" />
          </div>
          {/* Thay đổi 5: Sử dụng "DialogTitle" */}
          <DialogTitle>Đăng ký thành công!</DialogTitle>
          {/* Thay đổi 6: Sử dụng "DialogDescription" */}
          <DialogDescription className="text-center">
            Bạn đã đăng ký thành công! Vui lòng kiểm tra email để xác minh tài
            khoản của bạn.
          </DialogDescription>
        </DialogHeader>

        {/* Thay đổi 7: Thêm phần "Lưu ý:" còn thiếu */}
        <div className="text-center text-sm text-muted-foreground">Lưu ý:</div>

        {/* Thay đổi 8: Sử dụng "DialogFooter" và chỉnh sửa class */}
        {/* Bỏ "flex-col" và "w-full" để các button nằm ngang */}
        <DialogFooter className="flex-col-reverse gap-2 sm:flex-row sm:justify-center">
          {/* Thay đổi 9: Đảo thứ tự và style button cho đúng thiết kế */}
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

export { SignUpSuccessDialog };
