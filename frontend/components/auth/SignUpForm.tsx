"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { LoaderCircleIcon } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";

import { InputPassword } from "@/components/common/InputPassword";
import { InputWithIcon } from "@/components/common/InputWithIcon";
import { SignUpSuccessDialog } from "@/components/common/SignUpSuccessDialog";
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
  signUpSchema,
  type SignUpFormData,
} from "@/schemaValidations/signUpSchema";
import { supabase } from "@/utils/supabaseClient";

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
      <Card className="shadow-lg">
        <CardContent className="p-6">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="fullName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>{authMessages.labels.fullName}</FormLabel>
                    <FormControl>
                      <InputWithIcon
                        type="text"
                        placeholder="Nguyễn Văn A"
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
                    <FormLabel>{authMessages.labels.email}</FormLabel>
                    <FormControl>
                      <InputWithIcon
                        type="email"
                        placeholder="example@email.com"
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
                    <FormLabel>{authMessages.labels.password}</FormLabel>
                    <FormControl>
                      <InputPassword
                        placeholder="Nhập mật khẩu (8-30 ký tự)"
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
                    <FormLabel>{authMessages.labels.confirmPassword}</FormLabel>
                    <FormControl>
                      <InputPassword
                        placeholder="Xác nhận mật khẩu"
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
                {form.formState.isSubmitting ? (
                  <>
                    <LoaderCircleIcon className="animate-spin mr-2 h-4 w-4" />
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
