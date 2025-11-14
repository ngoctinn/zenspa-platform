"use client";

import { SetNewPasswordForm } from "@/components/auth/SetNewPasswordForm";

const ResetPasswordPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--background)]">
      <div className="max-w-md w-full space-y-8 p-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-[var(--foreground)]">
            Đặt lại mật khẩu
          </h2>
          <p className="mt-2 text-sm text-[var(--muted-foreground)]">
            Nhập mật khẩu mới cho tài khoản của bạn
          </p>
        </div>

        <SetNewPasswordForm />
      </div>
    </div>
  );
};

export default ResetPasswordPage;
