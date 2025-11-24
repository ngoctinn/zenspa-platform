"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { LoaderCircleIcon } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";

import { InputPassword } from "@/components/common/input-password";
import { InputWithIcon } from "@/components/common/input-with-icon";
import { SignUpSuccessDialog } from "@/components/common/sign-up-success-dialog";
import { showToast } from "@/components/common/toast";
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
  signUpSchema,
  type SignUpFormData,
} from "@/schemaValidations/signUpSchema";
import { createSupabaseBrowserClient } from "@/utils/supabaseClient";

interface SignUpFormProps {
  onSignUpSuccess?: () => void;
}

const SignUpForm = ({ onSignUpSuccess }: SignUpFormProps) => {
  const [showSuccessDialog, setShowSuccessDialog] = useState(false);

  const form = useForm<SignUpFormData>({
    resolver: zodResolver(signUpSchema),
    mode: "onChange",
    defaultValues: {
      fullName: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  const onSubmit = async (data: SignUpFormData) => {
    try {
      const supabase = createSupabaseBrowserClient();
      const { error } = await supabase.auth.signUp({
        email: data.email,
        password: data.password,
        options: {
          data: {
            full_name: data.fullName,
            role: "customer",
          },
        },
      });

      if (error) {
        if (error.message.includes("already registered")) {
          showToast({
            message: authMessages.errors.emailAlreadyExists,
            variant: "error",
          });
        } else {
          showToast({
            message: authMessages.errors.signUpFailed,
            variant: "error",
          });
        }
        return;
      }

      setShowSuccessDialog(true);
    } catch {
      showToast({
        message: authMessages.errors.networkError,
        variant: "error",
      });
    }
  };

  const handleGoHome = () => {
    setShowSuccessDialog(false);
    if (onSignUpSuccess) {
      onSignUpSuccess();
    }
  };

  return (
    <>
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
                name="fullName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-base font-medium">
                      {authMessages.labels.fullName}
                    </FormLabel>
                    <FormControl>
                      <InputWithIcon
                        type="text"
                        placeholder="Nhập họ và tên của bạn"
                        className="h-12 text-base"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

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
                        className="h-12 text-base"
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
                        placeholder="Nhập mật khẩu (8-30 ký tự)"
                        className="h-12 text-base"
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
                    <FormLabel className="text-base font-medium">
                      {authMessages.labels.confirmPassword}
                    </FormLabel>
                    <FormControl>
                      <InputPassword
                        placeholder="Xác nhận mật khẩu"
                        className="h-12 text-base"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button
                type="submit"
                className="w-full h-11 text-base font-semibold shadow-md hover:shadow-lg transition-all"
                disabled={form.formState.isSubmitting}
              >
                {form.formState.isSubmitting ? (
                  <>
                    <LoaderCircleIcon className="animate-spin mr-2 h-5 w-5" />
                    Đang đăng ký...
                  </>
                ) : (
                  authMessages.labels.signUp
                )}
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>

      <SignUpSuccessDialog
        open={showSuccessDialog}
        onOpenChange={setShowSuccessDialog}
        onGoHome={handleGoHome}
      />
    </>
  );
};

export { SignUpForm };
