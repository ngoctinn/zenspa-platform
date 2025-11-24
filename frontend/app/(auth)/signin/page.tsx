"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

import { SignInForm } from "@/components/auth/sign-in-form";

const SignInPage = () => {
  const router = useRouter();

  const handleSignInSuccess = () => {
    router.push("/"); // Redirect to home after sign in
  };

  const handleForgotPassword = () => {
    router.push("/forgot-password");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--background)]">
      <div className="max-w-md w-full space-y-8 p-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-[var(--foreground)]">
            Đăng nhập
          </h2>
        </div>

        <SignInForm
          onSignInSuccess={handleSignInSuccess}
          onForgotPassword={handleForgotPassword}
        />

        <div className="text-center">
          <p className="text-sm text-[var(--muted-foreground)]">
            Chưa có tài khoản?{" "}
            <Link
              href="/signup"
              className="font-medium text-[var(--primary)] hover:text-[var(--primary)]/80"
            >
              Đăng ký ngay
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignInPage;
