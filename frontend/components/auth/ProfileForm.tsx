"use client";

import { getUserProfile, updateUserProfile } from "@/apiRequests/user";
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
import {
  profileSchema,
  type ProfileFormData,
} from "@/schemaValidations/profileSchema";
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

export default function ProfileForm() {
  const [user, setUser] = useState<User | null>(null);
  const [avatarUrl, setAvatarUrl] = useState<string>("");
  const [uploading, setUploading] = useState(false);

  const form = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    mode: "onSubmit",
    defaultValues: {
      email: "",
      fullName: "",
      phone: "",
      birthDate: "",
    },
  });

  useEffect(() => {
    const getUser = async () => {
      try {
        const { data } = await supabase.auth.getUser();
        if (data.user) {
          setUser(data.user);
          // Load profile from API
          const profile = await getUserProfile();
          form.setValue("email", profile.email);
          form.setValue("fullName", profile.full_name || "");
          form.setValue("phone", profile.phone || "");
          form.setValue("birthDate", profile.birth_date || "");
          setAvatarUrl(profile.avatar_url || "");
        }
      } catch (error) {
        console.error("Failed to load profile:", error);
        toast.error("Không thể tải hồ sơ");
      }
    };
    getUser();
  }, [form]);

  const onSubmit = async (data: ProfileFormData) => {
    try {
      await updateUserProfile({
        full_name: data.fullName || null,
        phone: data.phone || null,
        birth_date: data.birthDate || null,
        avatar_url: avatarUrl || null,
      });
      toast.success("Cập nhật hồ sơ thành công!");
      // Reload profile data to sync with navbar
      const updatedProfile = await getUserProfile();
      form.setValue("email", updatedProfile.email);
      form.setValue("fullName", updatedProfile.full_name || "");
      form.setValue("phone", updatedProfile.phone || "");
      form.setValue("birthDate", updatedProfile.birth_date || "");
      setAvatarUrl(updatedProfile.avatar_url || "");
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
      // Note: Avatar URL will be saved when form is submitted
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
