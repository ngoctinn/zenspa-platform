import { z } from "zod";

export const profileSchema = z.object({
  email: z.string().email().optional(),
  fullName: z.string().min(1, "Họ và tên là bắt buộc"),
  phone: z.string().min(10, "Số điện thoại phải có ít nhất 10 ký tự"),
  birthDate: z.string().optional(),
});

export type ProfileFormData = z.infer<typeof profileSchema>;
