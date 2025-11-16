import { z } from "zod";

export const profileSchema = z.object({
  email: z.string().email().optional(),
  fullName: z.string().min(1, "Họ và tên là bắt buộc"),
  phone: z
    .string()
    .optional()
    .refine(
      (val) => !val || /^\+?\d{10,15}$/.test(val),
      "Số điện thoại không hợp lệ"
    ),
  birthDate: z
    .string()
    .optional()
    .refine((val) => {
      if (!val) return true;
      const date = new Date(val);
      const minDate = new Date(1900, 0, 1);
      return date >= minDate && !isNaN(date.getTime());
    }, "Ngày sinh không hợp lệ"),
});

export type ProfileFormData = z.infer<typeof profileSchema>;
