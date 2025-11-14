"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { InputPassword } from "@/components/common/InputPassword";
import { showToast } from "@/components/common/Toast";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { authMessages } from "@/lib/messages";
import {
  setNewPasswordSchema,
  type SetNewPasswordFormData,
} from "@/schemaValidations/setNewPasswordSchema";
import { supabase } from "@/utils/supabaseClient";

const SetNewPasswordForm = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isValidSession, setIsValidSession] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const form = useForm<SetNewPasswordFormData>({
    resolver: zodResolver(setNewPasswordSchema),
    mode: "onChange",
    defaultValues: {
      password: "",
      confirmPassword: "",
    },
  });

  useEffect(() => {
    const checkSession = async () => {
      const accessToken = searchParams.get("access_token");
      const refreshToken = searchParams.get("refresh_token");
      const type = searchParams.get("type");

      if (!accessToken || !refreshToken || type !== "recovery") {
        showToast({
          message: "Link reset mật khẩu không hợp lệ hoặc đã hết hạn",
          variant: "error",
        });
        router.push("/signin");
        return;
      }

      // Set session with tokens from URL
      const { error } = await supabase.auth.setSession({
        access_token: accessToken,
        refresh_token: refreshToken,
      });

      if (error) {
        showToast({
          message: "Phiên reset mật khẩu không hợp lệ",
          variant: "error",
        });
        router.push("/signin");
        return;
      }

      setIsValidSession(true);
      setIsLoading(false);
    };

    checkSession();
  }, [searchParams, router]);

  const onSubmit = async (data: SetNewPasswordFormData) => {
    try {
      const { error } = await supabase.auth.updateUser({
        password: data.password,
      });

      if (error) {
        showToast({
          message: authMessages.errors.resetPasswordFailed,
          variant: "error",
        });
        return;
      }

      showToast({
        message: authMessages.success.passwordResetSuccess,
        variant: "success",
      });

      // Redirect to signin after successful password reset
      router.push("/signin");
    } catch {
      showToast({
        message: authMessages.errors.networkError,
        variant: "error",
      });
    }
  };

  if (isLoading) {
    return (
      <Card className="shadow-lg">
        <CardContent className="p-6">
          <div className="text-center">
            <p>Đang xác minh link reset...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!isValidSession) {
    return null; // Will redirect
  }

  return (
    <Card className="shadow-lg">
      <CardContent className="p-6">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>{authMessages.labels.newPassword}</FormLabel>
                  <FormControl>
                    <InputPassword
                      placeholder="Nhập mật khẩu mới (8-30 ký tự)"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="confirmPassword"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>
                    {authMessages.labels.confirmNewPassword}
                  </FormLabel>
                  <FormControl>
                    <InputPassword
                      placeholder="Xác nhận mật khẩu mới"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type="submit"
              className="w-full"
              disabled={form.formState.isSubmitting}
            >
              {authMessages.labels.setNewPassword}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export { SetNewPasswordForm };
