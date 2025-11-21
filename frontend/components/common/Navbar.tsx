"use client";

import AuthActions from "@/components/auth/AuthActions";
import NotificationIcon from "@/components/auth/NotificationIcon";
import { UserProfileMenu } from "@/components/auth/UserProfileMenu";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { supabase } from "@/utils/supabaseClient";
import { User } from "@supabase/supabase-js";
import { Menu } from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const Navbar = () => {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [notificationCount] = useState(5); // Mock count, sẽ thay bằng API sau
  const pathname = usePathname();
  const [scrollY, setScrollY] = useState(0);
  const [scrollDirection, setScrollDirection] = useState<"up" | "down">("up");
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const getUser = async () => {
      setLoading(true);
      const { data } = await supabase.auth.getUser();
      setUser(data.user);
      setLoading(false);
    };
    getUser();
  }, []);

  useEffect(() => {
    let lastScrollY = window.scrollY;

    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      if (currentScrollY > lastScrollY) {
        setScrollDirection("down");
      } else {
        setScrollDirection("up");
      }
      setScrollY(currentScrollY);
      lastScrollY = currentScrollY;
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    setUser(null);
    router.push("/signin");
  };

  // Xác định className cho header dựa trên trạng thái cuộn
  const isNavbarVisible = scrollDirection === "up" || scrollY < 50;

  return (
    <header
      className={`sticky top-0 z-50 transition-transform duration-300 ${
        isNavbarVisible ? "translate-y-0" : "-translate-y-full"
      } ${
        scrollY > 0
          ? "bg-primary text-primary-foreground shadow-md"
          : "bg-primary text-primary-foreground"
      }`}
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center">
          {/* Logo and Navigation */}
          <div className="flex items-center space-x-4 md:space-x-8">
            {/* Mobile Menu */}
            <div className="md:hidden">
              <Sheet open={isOpen} onOpenChange={setIsOpen}>
                <SheetTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="text-primary-foreground hover:bg-primary-foreground/10"
                  >
                    <Menu className="h-6 w-6" />
                  </Button>
                </SheetTrigger>
                <SheetContent side="left" className="w-[300px] sm:w-[400px]">
                  <SheetHeader>
                    <SheetTitle className="text-left font-bold text-2xl text-primary">
                      ZENSPA
                    </SheetTitle>
                  </SheetHeader>
                  <Separator className="my-4" />
                  <div className="flex flex-col space-y-4 px-4">
                    <Link
                      href="/"
                      onClick={() => setIsOpen(false)}
                      className={`text-lg font-medium hover:text-primary transition-colors ${
                        pathname === "/" ? "text-primary" : "text-foreground/80"
                      }`}
                    >
                      Trang chủ
                    </Link>
                    <Link
                      href="#services"
                      onClick={() => setIsOpen(false)}
                      className="text-lg font-medium text-foreground/80 hover:text-primary transition-colors"
                    >
                      Dịch vụ
                    </Link>
                    <Link
                      href="#about"
                      onClick={() => setIsOpen(false)}
                      className="text-lg font-medium text-foreground/80 hover:text-primary transition-colors"
                    >
                      Về chúng tôi
                    </Link>
                    <Link
                      href="#contact"
                      onClick={() => setIsOpen(false)}
                      className="text-lg font-medium text-foreground/80 hover:text-primary transition-colors"
                    >
                      Liên hệ
                    </Link>
                  </div>
                </SheetContent>
              </Sheet>
            </div>

            <div className="flex items-center">
              <Link
                href="/"
                className="font-bold text-2xl md:text-4xl text-primary-foreground"
              >
                ZENSPA
              </Link>
            </div>

            {/* Main Navigation */}
            <nav className="hidden md:flex items-center space-x-6">
              <Link
                href="/"
                className={`font-semibold hover:underline transition-all duration-200 ${
                  pathname === "/" ? "font-bold" : "opacity-70"
                }`}
              >
                Trang chủ
              </Link>
              <Link
                href="#services"
                className="font-semibold opacity-70 hover:underline transition-all duration-200"
              >
                Dịch vụ
              </Link>
              <Link
                href="#about"
                className="font-semibold opacity-70 hover:underline transition-all duration-200"
              >
                Về chúng tôi
              </Link>
              <Link
                href="#contact"
                className="font-semibold opacity-70 hover:underline transition-all duration-200"
              >
                Liên hệ
              </Link>
            </nav>
          </div>

          {/* Actions & User Area */}
          <div className="ml-auto">
            {loading ? (
              <div className="flex items-center space-x-4">
                <div className="w-8 h-8 rounded-full animate-pulse"></div>
                <div className="w-20 h-4 rounded animate-pulse"></div>
              </div>
            ) : user ? (
              <div className="flex items-center space-x-4">
                <NotificationIcon count={notificationCount} />
                <UserProfileMenu user={user} onLogout={handleLogout} />
              </div>
            ) : (
              <AuthActions />
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
