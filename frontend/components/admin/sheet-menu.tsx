"use client";

import { MenuIcon, PanelsTopLeft } from "lucide-react";
import Link from "next/link";

import { useAdmin } from "@/components/admin/admin-context";
import { Menu } from "@/components/admin/menu";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { useEffect, useState } from "react";

export function SheetMenu() {
  const { user } = useAdmin();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return (
      <Button className="h-8 lg:hidden" variant="outline" size="icon">
        <MenuIcon size={20} />
      </Button>
    );
  }

  return (
    <Sheet>
      <SheetTrigger className="lg:hidden" asChild>
        <Button className="h-8" variant="outline" size="icon">
          <MenuIcon size={20} />
        </Button>
      </SheetTrigger>
      <SheetContent className="sm:w-72 px-3 h-full flex flex-col" side="left">
        <SheetHeader>
          <Button
            className="flex justify-center items-center pb-2 pt-1"
            variant="link"
            asChild
          >
            <Link href="/admin/dashboard" className="flex items-center gap-2">
              <PanelsTopLeft className="w-6 h-6 mr-1" />
              <SheetTitle className="font-bold text-lg">
                ZenSpa Admin
              </SheetTitle>
            </Link>
          </Button>
        </SheetHeader>
        <Menu isOpen userRoles={user?.roles} />
      </SheetContent>
    </Sheet>
  );
}
