"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CalendarIcon, ClockIcon, UserIcon } from "lucide-react";

// Mock data - replace with Supabase fetch later
const mockAppointments = [
  {
    id: 1,
    date: "2024-01-15",
    time: "10:00",
    service: "Massage toàn thân",
    therapist: "Nguyễn Thị A",
    status: "upcoming",
  },
  {
    id: 2,
    date: "2024-01-10",
    time: "14:00",
    service: "Chăm sóc da mặt",
    therapist: "Trần Thị B",
    status: "completed",
  },
];

export default function AppointmentsPage() {
  const upcomingAppointments = mockAppointments.filter(
    (apt) => apt.status === "upcoming"
  );
  const pastAppointments = mockAppointments.filter(
    (apt) => apt.status === "completed"
  );

  const AppointmentCard = ({
    appointment,
  }: {
    appointment: (typeof mockAppointments)[0];
  }) => (
    <Card className="mb-4">
      <CardContent className="p-4">
        <div className="flex justify-between items-start">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <CalendarIcon className="h-4 w-4" />
              <span className="font-medium">{appointment.date}</span>
              <ClockIcon className="h-4 w-4 ml-2" />
              <span>{appointment.time}</span>
            </div>
            <div className="flex items-center gap-2">
              <UserIcon className="h-4 w-4" />
              <span>{appointment.service}</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Chuyên viên: {appointment.therapist}
            </p>
          </div>
          <div className="flex flex-col items-end gap-2">
            <Badge
              variant={
                appointment.status === "upcoming" ? "default" : "secondary"
              }
            >
              {appointment.status === "upcoming" ? "Sắp tới" : "Đã hoàn thành"}
            </Badge>
            {appointment.status === "upcoming" && (
              <Button variant="outline" size="sm">
                Hủy lịch
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Lịch hẹn của tôi</h1>
        <p className="text-muted-foreground">
          Quản lý các lịch hẹn Spa của bạn
        </p>
      </div>

      <Tabs defaultValue="all" className="w-full">
        <TabsList>
          <TabsTrigger value="all">Tất cả</TabsTrigger>
          <TabsTrigger value="upcoming">Sắp tới</TabsTrigger>
          <TabsTrigger value="past">Đã qua</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          {mockAppointments.map((apt) => (
            <AppointmentCard key={apt.id} appointment={apt} />
          ))}
        </TabsContent>

        <TabsContent value="upcoming" className="space-y-4">
          {upcomingAppointments.map((apt) => (
            <AppointmentCard key={apt.id} appointment={apt} />
          ))}
        </TabsContent>

        <TabsContent value="past" className="space-y-4">
          {pastAppointments.map((apt) => (
            <AppointmentCard key={apt.id} appointment={apt} />
          ))}
        </TabsContent>
      </Tabs>
    </div>
  );
}
