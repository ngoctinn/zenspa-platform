"use client";

import SidebarMenu from "@/components/auth/SidebarMenu";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Menu, X } from "lucide-react";
import { useState } from "react";

export default function AccountLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [showSidebar, setShowSidebar] = useState(false);

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Mobile Menu Toggle */}
      <div className="lg:hidden mb-4">
        <Button
          variant="outline"
          onClick={() => setShowSidebar(!showSidebar)}
          className="flex items-center space-x-2"
        >
          {showSidebar ? (
            <X className="h-4 w-4" />
          ) : (
            <Menu className="h-4 w-4" />
          )}
          <span>Menu Tài Khoản</span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar - Cột trái */}
        <div
          className={`lg:col-span-1 ${
            showSidebar ? "block" : "hidden"
          } lg:block`}
        >
          <Card className="p-4">
            <h2 className="text-lg font-semibold mb-4">Menu Tài Khoản</h2>
            <SidebarMenu />
          </Card>
        </div>

        {/* Content Area - Cột phải */}
        <div className="lg:col-span-3">
          <Card className="p-6">{children}</Card>
        </div>
      </div>
    </div>
  );
}
