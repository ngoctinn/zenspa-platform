"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { LoaderCircleIcon } from "lucide-react";
import { useForm } from "react-hook-form";

import { InputPassword } from "@/components/common/InputPassword";
import { InputWithIcon } from "@/components/common/InputWithIcon";
import { showToast } from "@/components/common/Toast";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
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
  signInSchema,
  type SignInFormData,
} from "@/schemaValidations/signInSchema";
import { supabase } from "@/utils/supabaseClient";

interface SignInFormProps {
  onSignInSuccess?: () => void;
  onForgotPassword?: () => void;
}

const SignInForm = ({ onSignInSuccess, onForgotPassword }: SignInFormProps) => {
  const form = useForm<SignInFormData>({
    resolver: zodResolver(signInSchema),
    mode: "onChange",
    defaultValues: {
      email: "",
      password: "",
      remember: false,
    },
  });

  const onSubmit = async (data: SignInFormData) => {
    try {
      const { error } = await supabase.auth.signInWithPassword({
        email: data.email,
        password: data.password,
      });

      if (error) {
        showToast({
          message: authMessages.errors.signInFailed,
          variant: "error",
        });
        return;
      }

      // Call API to set httpOnly cookie
      const { data: sessionData } = await supabase.auth.getSession();
      if (sessionData.session?.access_token) {
        await fetch("/api/auth/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            access_token: sessionData.session.access_token,
          }),
        });
      }

      showToast({
        message: authMessages.success.signInSuccess,
        variant: "success",
      });

      if (onSignInSuccess) {
        onSignInSuccess();
      }
    } catch {
      showToast({
        message: authMessages.errors.networkError,
        variant: "error",
      });
    }
  };

  return (
    <Card className="shadow-xl border-0 sm:min-w-[400px]">
      <CardContent className="p-8">
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="space-y-4"
            noValidate
          >
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-base font-medium">
                    {authMessages.labels.email}
                  </FormLabel>
                  <FormControl>
                    <InputWithIcon
                      type="email"
                      placeholder="Nhập email của bạn"
                      className="h-11 text-base"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-base font-medium">
                    {authMessages.labels.password}
                  </FormLabel>
                  <FormControl>
                    <InputPassword
                      placeholder="Nhập mật khẩu của bạn"
                      className="h-11 text-base"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="flex items-center justify-between pt-2">
              <FormField
                control={form.control}
                name="remember"
                render={({ field }) => (
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="remember"
                      checked={field.value}
                      onCheckedChange={field.onChange}
                      className="h-5 w-5"
                    />
                    <FormLabel
                      htmlFor="remember"
                      className="text-sm font-normal cursor-pointer"
                    >
                      {authMessages.labels.rememberMe}
                    </FormLabel>
                  </div>
                )}
              />
              <Button
                type="button"
                variant="link"
                className="p-0 h-auto text-sm font-medium text-primary hover:text-primary/80"
                onClick={onForgotPassword}
              >
                {authMessages.labels.forgotPassword}
              </Button>
            </div>

            <Button
              type="submit"
              className="w-full h-11 text-base font-semibold shadow-md hover:shadow-lg transition-all"
              disabled={form.formState.isSubmitting}
            >
              {form.formState.isSubmitting ? (
                <>
                  <LoaderCircleIcon className="animate-spin mr-2 h-5 w-5" />
                  Đang đăng nhập...
                </>
              ) : (
                authMessages.labels.signIn
              )}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export { SignInForm };
