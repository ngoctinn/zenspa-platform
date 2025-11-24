"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

import { SignUpForm } from "@/components/auth/sign-up-form";

const SignUpPage = () => {
  const router = useRouter();

  const handleSignUpSuccess = () => {
    router.push("/"); // Redirect to home after sign up success
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--background)]">
      <div className="max-w-md w-full space-y-8 p-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-[var(--foreground)]">
            Đăng ký tài khoản
          </h2>
        </div>

        <SignUpForm onSignUpSuccess={handleSignUpSuccess} />

        <div className="text-center">
          <p className="text-sm text-[var(--muted-foreground)]">
            Đã có tài khoản?{" "}
            <Link
              href="/signin"
              className="font-medium text-[var(--primary)] hover:text-[var(--primary)]/80"
            >
              Đăng nhập
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignUpPage;
