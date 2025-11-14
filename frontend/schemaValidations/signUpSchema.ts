import { z } from "zod";

export const signUpSchema = z
  .object({
    fullName: z
      .string()
      .min(1, "Họ và tên là bắt buộc")
      .min(2, "Họ và tên phải có ít nhất 2 ký tự"),
    email: z.string().min(1, "Email là bắt buộc").email("Email không hợp lệ"),
    password: z
      .string()
      .min(1, "Mật khẩu là bắt buộc")
      .min(8, "Mật khẩu phải có ít nhất 8 ký tự")
      .max(30, "Mật khẩu không được quá 30 ký tự"),
    confirmPassword: z.string().min(1, "Xác nhận mật khẩu là bắt buộc"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Mật khẩu xác nhận không khớp",
    path: ["confirmPassword"],
  });

export type SignUpFormData = z.infer<typeof signUpSchema>;
