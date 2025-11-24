"use client";

import { SetNewPasswordForm } from "@/components/auth/set-new-password-form";

const ResetPasswordPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--background)]">
      <div className="max-w-md w-full space-y-8 p-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-[var(--foreground)]">
            Đặt lại mật khẩu
          </h2>
        </div>

        <SetNewPasswordForm />
      </div>
    </div>
  );
};

export default ResetPasswordPage;
