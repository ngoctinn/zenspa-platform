"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

import { ResetPasswordForm } from "@/components/auth/reset-password-form";

const ForgotPasswordPage = () => {
  const router = useRouter();

  const handleSendResetSuccess = () => {
    // Stay on page or show message
  };

  const handleBackToSignIn = () => {
    router.push("/signin");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--background)]">
      <div className="max-w-md w-full space-y-8 p-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-[var(--foreground)]">
            Quên mật khẩu
          </h2>
        </div>

        <ResetPasswordForm
          onSendResetSuccess={handleSendResetSuccess}
          onBackToSignIn={handleBackToSignIn}
        />

        <div className="text-center">
          <Link
            href="/signin"
            className="text-sm font-medium text-[var(--primary)] hover:text-[var(--primary)]/80"
          >
            Quay lại đăng nhập
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
