"use client";

import { zodResolver } from "@hookform/resolvers/zod";
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
    <Card className="shadow-lg">
      <CardContent className="p-6">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
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
                    <InputPassword placeholder="Nhập mật khẩu" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="flex items-center justify-between">
              <FormField
                control={form.control}
                name="remember"
                render={({ field }) => (
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="remember"
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                    <FormLabel htmlFor="remember" className="text-sm">
                      {authMessages.labels.rememberMe}
                    </FormLabel>
                  </div>
                )}
              />
              <Button
                type="button"
                variant="link"
                className="p-0 h-auto"
                onClick={onForgotPassword}
              >
                {authMessages.labels.forgotPassword}
              </Button>
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={form.formState.isSubmitting}
            >
              {authMessages.labels.signIn}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export { SignInForm };
