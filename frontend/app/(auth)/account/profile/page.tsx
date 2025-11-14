"use client";

import ProfileForm from "@/components/auth/ProfileForm";

export default function ProfilePage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Thông tin cá nhân</h1>
      <p className="text-muted-foreground mb-8">
        Quản lý và cập nhật thông tin cá nhân của bạn.
      </p>
      <ProfileForm />
    </div>
  );
}
