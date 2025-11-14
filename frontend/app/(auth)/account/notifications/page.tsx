"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CheckIcon, TrashIcon } from "lucide-react";

// Mock data - replace with Supabase fetch later
const mockNotifications = [
  {
    id: 1,
    title: "Xác nhận lịch hẹn",
    message: "Lịch hẹn massage của bạn vào 15/01/2024 đã được xác nhận.",
    date: "2024-01-12",
    isRead: false,
  },
  {
    id: 2,
    title: "Khuyến mãi đặc biệt",
    message: "Giảm 20% cho gói massage tháng này. Đừng bỏ lỡ!",
    date: "2024-01-10",
    isRead: true,
  },
  {
    id: 3,
    title: "Nhắc nhở lịch hẹn",
    message: "Bạn có lịch hẹn vào ngày mai lúc 10:00. Hãy chuẩn bị nhé!",
    date: "2024-01-14",
    isRead: false,
  },
];

export default function NotificationsPage() {
  const unreadNotifications = mockNotifications.filter((n) => !n.isRead);
  const allNotifications = mockNotifications;

  const NotificationItem = ({
    notification,
  }: {
    notification: (typeof mockNotifications)[0];
  }) => (
    <Card className={`mb-4 ${!notification.isRead ? "border-primary" : ""}`}>
      <CardContent className="p-4">
        <div className="flex justify-between items-start">
          <div className="space-y-2 flex-1">
            <div className="flex items-center gap-2">
              <h3 className="font-medium">{notification.title}</h3>
              {!notification.isRead && (
                <Badge variant="destructive" className="text-xs">
                  Mới
                </Badge>
              )}
            </div>
            <p className="text-sm text-muted-foreground">
              {notification.message}
            </p>
            <p className="text-xs text-muted-foreground">{notification.date}</p>
          </div>
          <div className="flex gap-2 ml-4">
            {!notification.isRead && (
              <Button variant="ghost" size="sm">
                <CheckIcon className="h-4 w-4" />
              </Button>
            )}
            <Button variant="ghost" size="sm">
              <TrashIcon className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Thông báo</h1>
        <p className="text-muted-foreground">
          Xem các thông báo và cập nhật từ ZenSpa
        </p>
      </div>

      <Tabs defaultValue="all" className="w-full">
        <TabsList>
          <TabsTrigger value="all">
            Tất cả ({allNotifications.length})
          </TabsTrigger>
          <TabsTrigger value="unread">
            Chưa đọc ({unreadNotifications.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          {allNotifications.map((notif) => (
            <NotificationItem key={notif.id} notification={notif} />
          ))}
        </TabsContent>

        <TabsContent value="unread" className="space-y-4">
          {unreadNotifications.map((notif) => (
            <NotificationItem key={notif.id} notification={notif} />
          ))}
        </TabsContent>
      </Tabs>
    </div>
  );
}
