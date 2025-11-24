import { ContentLayout } from "@/components/admin/content-layout";
import { AdminUserManagementPage } from "@/components/admin/user-management-page";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Quản Lý Tài Khoản | ZenSpa Admin",
  description: "Quản lý tài khoản người dùng hệ thống",
};

export default function AdminUsersPage() {
  return (
    <ContentLayout title="Quản Lý Tài Khoản">
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink asChild>
              <Link href="/admin/dashboard">Dashboard</Link>
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Quản Lý Tài Khoản</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
      <div className="mt-6">
        <AdminUserManagementPage />
      </div>
    </ContentLayout>
  );
}
