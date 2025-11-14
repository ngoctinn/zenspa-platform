import { z } from "zod";

export const signInSchema = z.object({
  email: z.string().min(1, "Email là bắt buộc").email("Email không hợp lệ"),
  password: z
    .string()
    .min(1, "Mật khẩu là bắt buộc")
    .min(8, "Mật khẩu phải có ít nhất 8 ký tự")
    .max(30, "Mật khẩu không được quá 30 ký tự"),
  remember: z.boolean().optional(),
});

export type SignInFormData = z.infer<typeof signInSchema>;
