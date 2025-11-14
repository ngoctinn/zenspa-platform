"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { LoaderCircleIcon } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";

import { InputWithIcon } from "@/components/common/InputWithIcon";
import { ResetPasswordSuccessDialog } from "@/components/common/ResetPasswordSuccessDialog";
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
  const [showSuccessDialog, setShowSuccessDialog] = useState(false);

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
        redirectTo: `http://localhost:3000/reset-password`,
      });

      if (error) {
        showToast({
          message: authMessages.errors.resetFailed,
          variant: "error",
        });
        return;
      }

      setShowSuccessDialog(true);

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

  const handleGoHome = () => {
    setShowSuccessDialog(false);
  };

  return (
    <>
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
                {form.formState.isSubmitting ? (
                  <>
                    <LoaderCircleIcon className="animate-spin mr-2 h-4 w-4" />
                    Đang gửi...
                  </>
                ) : (
                  authMessages.labels.sendResetEmail
                )}
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

      <ResetPasswordSuccessDialog
        open={showSuccessDialog}
        onOpenChange={setShowSuccessDialog}
        onGoHome={handleGoHome}
      />
    </>
  );
};

export { ResetPasswordForm };
