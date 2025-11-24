"use client";

import { getUserProfile, updateUserProfile } from "@/apiRequests/user";
import { InputWithIcon } from "@/components/common/InputWithIcon";
import { showToast } from "@/components/common/Toast";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
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
import { createSupabaseBrowserClient } from "@/utils/supabaseClient";
import { zodResolver } from "@hookform/resolvers/zod";
import { User } from "@supabase/supabase-js";
import {
  BadgeCheck,
  CalendarIcon,
  CameraIcon,
  MailIcon,
  PhoneIcon,
  UserIcon,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

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
        const supabase = createSupabaseBrowserClient();
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
        showToast({
          message: "Lỗi tải dữ liệu",
          description: "Không thể tải thông tin hồ sơ. Vui lòng thử lại sau.",
          variant: "error",
        });
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
      showToast({
        message: "Cập nhật thành công",
        description: "Thông tin hồ sơ của bạn đã được lưu.",
        variant: "success",
      });
      // Reload profile data to sync with navbar
      const updatedProfile = await getUserProfile();
      form.setValue("email", updatedProfile.email);
      form.setValue("fullName", updatedProfile.full_name || "");
      form.setValue("phone", updatedProfile.phone || "");
      form.setValue("birthDate", updatedProfile.birth_date || "");
      setAvatarUrl(updatedProfile.avatar_url || "");
    } catch (error) {
      console.error("Update error:", error);
      showToast({
        message: "Cập nhật thất bại",
        description: "Đã có lỗi xảy ra khi lưu hồ sơ. Vui lòng thử lại.",
        variant: "error",
      });
    }
  };

  const uploadAvatar = async (event: React.ChangeEvent<HTMLInputElement>) => {
    try {
      setUploading(true);
      const file = event.target.files?.[0];
      if (!file || !user) return;

      const supabase = createSupabaseBrowserClient();
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
      showToast({
        message: "Upload thành công",
        description: "Ảnh đại diện mới đã được tải lên.",
        variant: "success",
      });
      // Note: Avatar URL will be saved when form is submitted
    } catch (error) {
      console.error("Upload error:", error);
      showToast({
        message: "Upload thất bại",
        description: "Không thể tải lên ảnh đại diện. Vui lòng kiểm tra lại.",
        variant: "error",
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto shadow-lg border-t-4 border-t-primary">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Hồ sơ cá nhân</CardTitle>
        <CardDescription>
          Quản lý thông tin cá nhân và cài đặt tài khoản của bạn.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <div className="flex flex-col md:flex-row gap-8">
              {/* Avatar Section - Left Side */}
              <div className="flex flex-col items-center space-y-4 md:w-1/3">
                <div className="relative group">
                  <Avatar className="w-32 h-32 border-4 border-background shadow-xl ring-2 ring-muted">
                    <AvatarImage
                      src={avatarUrl}
                      alt="Avatar"
                      className="object-cover"
                    />
                    <AvatarFallback className="text-4xl bg-muted">
                      {user?.email?.charAt(0).toUpperCase() || "U"}
                    </AvatarFallback>
                  </Avatar>
                  <Label
                    htmlFor="avatar-upload"
                    className="absolute bottom-0 right-0 p-2.5 bg-primary text-primary-foreground rounded-full cursor-pointer hover:bg-primary/90 transition-all shadow-md border-2 border-background group-hover:scale-110"
                  >
                    {uploading ? (
                      <div className="w-4 h-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                    ) : (
                      <CameraIcon className="w-4 h-4" />
                    )}
                  </Label>
                  <input
                    id="avatar-upload"
                    type="file"
                    accept="image/*"
                    onChange={uploadAvatar}
                    className="hidden"
                    disabled={uploading}
                  />
                </div>
                <div className="text-center space-y-1">
                  <p className="font-medium text-sm text-foreground">
                    Ảnh đại diện
                  </p>
                  <p className="text-xs text-muted-foreground">
                    JPG, PNG hoặc GIF. Tối đa 5MB.
                  </p>
                </div>
              </div>

              {/* Form Fields - Right Side */}
              <div className="flex-1 space-y-6">
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
                            className="bg-muted/50"
                            {...field}
                          />
                          {user?.email_confirmed_at && (
                            <BadgeCheck className="absolute right-3 top-1/2 transform -translate-y-1/2 text-green-600 size-4" />
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
                          placeholder="Nhập họ và tên của bạn"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                            placeholder="0123 456 789"
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
              </div>
            </div>

            <div className="flex justify-end space-x-4 pt-6 border-t">
              <Button type="button" variant="outline">
                Hủy bỏ
              </Button>
              <Button type="submit" disabled={form.formState.isSubmitting}>
                {form.formState.isSubmitting ? "Đang lưu..." : "Lưu thay đổi"}
              </Button>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
