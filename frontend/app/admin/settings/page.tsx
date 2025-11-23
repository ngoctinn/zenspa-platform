import { ContentLayout } from "@/components/admin/content-layout";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import Link from "next/link";

export default function SettingsPage() {
  return (
    <ContentLayout title="Cấu hình hệ thống">
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink asChild>
              <Link href="/admin/dashboard">Dashboard</Link>
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Cấu hình hệ thống</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
      <div className="mt-6 p-4 border rounded-lg border-dashed min-h-[400px] flex items-center justify-center bg-slate-50 dark:bg-slate-900/20">
        <h2 className="text-2xl font-bold">Nội dung trang Cấu hình hệ thống</h2>
      </div>
    </ContentLayout>
  );
}
