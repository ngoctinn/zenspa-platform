"use client";

import { InputWithIcon } from "@/components/common/InputWithIcon";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Label } from "@/components/ui/label";
import { supabase } from "@/utils/supabaseClient";
import { zodResolver } from "@hookform/resolvers/zod";
import { User } from "@supabase/supabase-js";
import {
  CalendarIcon,
  CheckIcon,
  MailIcon,
  PhoneIcon,
  UserIcon,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

const profileSchema = z.object({
  email: z.string().email().optional(),
  fullName: z.string().min(1, "Họ và tên là bắt buộc"),
  phone: z.string().min(10, "Số điện thoại phải có ít nhất 10 ký tự"),
  birthDate: z.string().optional(),
});

type ProfileFormData = z.infer<typeof profileSchema>;

export default function ProfileForm() {
  const [user, setUser] = useState<User | null>(null);
  const [avatarUrl, setAvatarUrl] = useState<string>("");
  const [uploading, setUploading] = useState(false);

  const form = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
  });

  useEffect(() => {
    const getUser = async () => {
      const { data } = await supabase.auth.getUser();
      if (data.user) {
        setUser(data.user);
        // Mock profile data, replace with API call
        form.setValue("email", data.user.email);
        form.setValue("fullName", "Nguyễn Văn A");
        form.setValue("phone", "0123456789");
        form.setValue("birthDate", "1990-01-01");
        setAvatarUrl("https://via.placeholder.com/150");
      }
    };
    getUser();
  }, [form]);

  const onSubmit = async (data: ProfileFormData) => {
    try {
      console.log("Updating profile:", data);
      // TODO: Send to API
      toast.success("Cập nhật hồ sơ thành công!");
    } catch (error) {
      console.error("Update error:", error);
      toast.error("Lỗi cập nhật hồ sơ");
    }
  };

  const uploadAvatar = async (event: React.ChangeEvent<HTMLInputElement>) => {
    try {
      setUploading(true);
      const file = event.target.files?.[0];
      if (!file || !user) return;

      const fileExt = file.name.split(".").pop();
      const fileName = `${user.id}.${fileExt}`;
      const { data, error } = await supabase.storage
        .from("avatars")
        .upload(fileName, file);

      if (error) throw error;

      console.log("Upload success:", data);

      const { data: urlData } = supabase.storage
        .from("avatars")
        .getPublicUrl(fileName);

      setAvatarUrl(urlData.publicUrl);
      toast.success("Upload avatar thành công!");
    } catch (error) {
      console.error("Upload error:", error);
      toast.error("Lỗi upload avatar");
    } finally {
      setUploading(false);
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* Avatar Section */}
        <div className="flex items-center space-x-4">
          <Avatar className="w-20 h-20">
            <AvatarImage src={avatarUrl} alt="Avatar" />
            <AvatarFallback>AV</AvatarFallback>
          </Avatar>
          <div>
            <Label htmlFor="avatar-upload" className="cursor-pointer">
              <Button type="button" variant="outline" disabled={uploading}>
                {uploading ? "Đang upload..." : "Thay đổi ảnh đại diện"}
              </Button>
            </Label>
            <input
              id="avatar-upload"
              type="file"
              accept="image/*"
              onChange={uploadAvatar}
              className="hidden"
            />
          </div>
        </div>

        {/* Form Fields */}
        <div className="grid grid-cols-1 gap-4">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <div className="relative">
                    <InputWithIcon
                      type="email"
                      icon={<MailIcon className="size-4" />}
                      disabled
                      {...field}
                    />
                    {user?.email_confirmed_at && (
                      <CheckIcon className="absolute right-3 top-1/2 transform -translate-y-1/2 text-green-500 size-4" />
                    )}
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="fullName"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Họ và tên</FormLabel>
                <FormControl>
                  <InputWithIcon
                    icon={<UserIcon className="size-4" />}
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="phone"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Số điện thoại</FormLabel>
                <FormControl>
                  <InputWithIcon
                    type="tel"
                    icon={<PhoneIcon className="size-4" />}
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="birthDate"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Ngày sinh</FormLabel>
                <FormControl>
                  <InputWithIcon
                    type="date"
                    icon={<CalendarIcon className="size-4" />}
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        {/* Actions */}
        <div className="flex space-x-4">
          <Button type="submit" disabled={form.formState.isSubmitting}>
            {form.formState.isSubmitting ? "Đang lưu..." : "Lưu thay đổi"}
          </Button>
          <Button type="button" variant="outline">
            Hủy
          </Button>
        </div>
      </form>
    </Form>
  );
}
