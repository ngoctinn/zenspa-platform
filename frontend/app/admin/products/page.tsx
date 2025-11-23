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

export default function ProductsPage() {
  return (
    <ContentLayout title="Sản phẩm">
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink asChild>
              <Link href="/admin/dashboard">Dashboard</Link>
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Sản phẩm</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
      <div className="mt-6 p-4 border rounded-lg border-dashed min-h-[400px] flex items-center justify-center bg-indigo-50 dark:bg-indigo-900/20">
        <h2 className="text-2xl font-bold">Nội dung trang Sản phẩm</h2>
      </div>
    </ContentLayout>
  );
}
