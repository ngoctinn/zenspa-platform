"use client";

import AuthActions from "@/components/auth/AuthActions";
import NotificationIcon from "@/components/auth/NotificationIcon";
import { UserProfileMenu } from "@/components/auth/UserProfileMenu";
import { supabase } from "@/utils/supabaseClient";
import { User } from "@supabase/supabase-js";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const Navbar = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [notificationCount] = useState(5); // Mock count, sẽ thay bằng API sau
  const pathname = usePathname();

  useEffect(() => {
    const getUser = async () => {
      setLoading(true);
      const { data } = await supabase.auth.getUser();
      setUser(data.user);
      setLoading(false);
    };
    getUser();
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    setUser(null);
  };

  return (
    <header className="sticky top-0 z-50 bg-primary text-primary-foreground">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center">
          {/* Logo and Navigation */}
          <div className="flex items-center space-x-8">
            <div className="flex items-center">
              <Link
                href="/"
                className="font-bold text-2xl text-primary-foreground"
              >
                ZENSPA
              </Link>
            </div>

            {/* Main Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              <Link
                href="/"
                className={`font-semibold relative transition-all duration-200 ease-in-out group ${
                  pathname === "/" ? "font-bold" : "opacity-70"
                }`}
              >
                Trang chủ
                <svg
                  width="60"
                  height="4"
                  viewBox="0 0 60 4"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="absolute inset-x-0 bottom-0 w-full translate-y-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200 ease-in-out"
                >
                  <path
                    d="M1 2.5C10 1 20 0.5 30 1C40 1.5 50 2 59 2.5"
                    stroke="url(#nav-gradient)"
                    strokeWidth="2"
                    strokeLinecap="round"
                  />
                  <defs>
                    <linearGradient
                      id="nav-gradient"
                      x1="0%"
                      y1="0%"
                      x2="100%"
                      y2="0%"
                    >
                      <stop stopColor="var(--primary-foreground)" />
                      <stop offset="1" stopColor="var(--primary-foreground)" />
                    </linearGradient>
                  </defs>
                </svg>
              </Link>
              <Link
                href="#services"
                className="font-semibold opacity-70 relative transition-all duration-200 ease-in-out group"
              >
                Dịch vụ
                <svg
                  width="50"
                  height="4"
                  viewBox="0 0 50 4"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="absolute inset-x-0 bottom-0 w-full translate-y-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200 ease-in-out"
                >
                  <path
                    d="M1 2.5C8 1 16 0.5 25 1C34 1.5 42 2 49 2.5"
                    stroke="url(#nav-gradient)"
                    strokeWidth="2"
                    strokeLinecap="round"
                  />
                  <defs>
                    <linearGradient
                      id="nav-gradient"
                      x1="0%"
                      y1="0%"
                      x2="100%"
                      y2="0%"
                    >
                      <stop stopColor="var(--primary-foreground)" />
                      <stop offset="1" stopColor="var(--primary-foreground)" />
                    </linearGradient>
                  </defs>
                </svg>
              </Link>
              <Link
                href="#about"
                className="font-semibold opacity-70 relative transition-all duration-200 ease-in-out flex items-center group"
              >
                Về chúng tôi
                <svg
                  width="80"
                  height="4"
                  viewBox="0 0 80 4"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="absolute inset-x-0 bottom-0 w-full translate-y-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200 ease-in-out"
                >
                  <path
                    d="M1 2.5C13 1 27 0.5 40 1C53 1.5 67 2 79 2.5"
                    stroke="url(#nav-gradient)"
                    strokeWidth="2"
                    strokeLinecap="round"
                  />
                  <defs>
                    <linearGradient
                      id="nav-gradient"
                      x1="0%"
                      y1="0%"
                      x2="100%"
                      y2="0%"
                    >
                      <stop stopColor="var(--primary-foreground)" />
                      <stop offset="1" stopColor="var(--primary-foreground)" />
                    </linearGradient>
                  </defs>
                </svg>
              </Link>
              <Link
                href="#contact"
                className="font-semibold opacity-70 relative transition-all duration-200 ease-in-out group"
              >
                Liên hệ
                <svg
                  width="55"
                  height="4"
                  viewBox="0 0 55 4"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="absolute inset-x-0 bottom-0 w-full translate-y-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200 ease-in-out"
                >
                  <path
                    d="M1 2.5C9 1 18 0.5 27.5 1C37 1.5 46 2 54 2.5"
                    stroke="url(#nav-gradient)"
                    strokeWidth="2"
                    strokeLinecap="round"
                  />
                  <defs>
                    <linearGradient
                      id="nav-gradient"
                      x1="0%"
                      y1="0%"
                      x2="100%"
                      y2="0%"
                    >
                      <stop stopColor="var(--primary-foreground)" />
                      <stop offset="1" stopColor="var(--primary-foreground)" />
                    </linearGradient>
                  </defs>
                </svg>
              </Link>
            </nav>
          </div>

          {/* Actions & User Area */}
          <div className="ml-auto">
            {loading ? (
              <div className="flex items-center space-x-4">
                <div className="w-8 h-8 bg-gray-300 rounded-full animate-pulse"></div>
                <div className="w-20 h-4 bg-gray-300 rounded animate-pulse"></div>
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
