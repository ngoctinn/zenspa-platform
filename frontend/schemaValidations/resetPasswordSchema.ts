import { z } from "zod";

export const resetPasswordSchema = z.object({
  email: z.string().min(1, "Email là bắt buộc").email("Email không hợp lệ"),
});

export type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>;
