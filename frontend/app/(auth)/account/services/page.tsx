"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { PackageIcon } from "lucide-react";

// Mock data - replace with Supabase fetch later
const mockServices = [
  {
    id: 1,
    name: "Gói Massage toàn thân 10 buổi",
    description: "Massage thư giãn toàn thân chuyên nghiệp",
    totalSessions: 10,
    usedSessions: 3,
    expiryDate: "2024-12-31",
  },
  {
    id: 2,
    name: "Gói Chăm sóc da mặt 5 buổi",
    description: "Chăm sóc da chuyên sâu",
    totalSessions: 5,
    usedSessions: 5,
    expiryDate: "2024-06-30",
  },
];

export default function ServicesPage() {
  const ServiceCard = ({ service }: { service: (typeof mockServices)[0] }) => {
    const remainingSessions = service.totalSessions - service.usedSessions;
    const progressValue = (service.usedSessions / service.totalSessions) * 100;

    return (
      <Card className="mb-4">
        <CardContent className="p-4">
          <div className="flex justify-between items-start mb-4">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <PackageIcon className="h-5 w-5" />
                <h3 className="font-semibold">{service.name}</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                {service.description}
              </p>
              <p className="text-sm">Hết hạn: {service.expiryDate}</p>
            </div>
            <Button variant="outline" size="sm">
              Mua thêm
            </Button>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>
                Đã sử dụng: {service.usedSessions}/{service.totalSessions}
              </span>
              <span>Còn lại: {remainingSessions}</span>
            </div>
            <Progress value={progressValue} className="h-2" />
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Gói dịch vụ</h1>
        <p className="text-muted-foreground">
          Quản lý các gói dịch vụ và liệu trình đã mua
        </p>
      </div>

      <div className="space-y-4">
        {mockServices.map((service) => (
          <ServiceCard key={service.id} service={service} />
        ))}
      </div>
    </div>
  );
}
