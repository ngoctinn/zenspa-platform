"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import { InputWithIcon } from "@/components/common/InputWithIcon";
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
  resetPasswordSchema,
  type ResetPasswordFormData,
} from "@/schemaValidations/resetPasswordSchema";
import { supabase } from "@/utils/supabaseClient";

interface ResetPasswordFormProps {
  onSendResetSuccess?: () => void;
  onBackToSignIn?: () => void;
}

const ResetPasswordForm = ({
  onSendResetSuccess,
  onBackToSignIn,
}: ResetPasswordFormProps) => {
  const form = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
    mode: "onChange",
    defaultValues: {
      email: "",
    },
  });

  const onSubmit = async (data: ResetPasswordFormData) => {
    try {
      const { error } = await supabase.auth.resetPasswordForEmail(data.email, {
        redirectTo: `${window.location.origin}/reset-password`,
      });

      if (error) {
        showToast({
          message: authMessages.errors.resetFailed,
          variant: "error",
        });
        return;
      }

      showToast({
        message: authMessages.success.resetEmailSent,
        variant: "success",
      });

      if (onSendResetSuccess) {
        onSendResetSuccess();
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

            <Button
              type="submit"
              className="w-full"
              disabled={form.formState.isSubmitting}
            >
              {authMessages.labels.sendResetEmail}
            </Button>

            {onBackToSignIn && (
              <Button
                type="button"
                variant="outline"
                className="w-full"
                onClick={onBackToSignIn}
              >
                {authMessages.labels.backToSignIn}
              </Button>
            )}
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export { ResetPasswordForm };
