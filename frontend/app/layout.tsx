import type { Metadata } from "next";
import { Be_Vietnam_Pro, Roboto_Mono, Wittgenstein } from "next/font/google";
import { Toaster } from "sonner";
import "./globals.css";

const fontSans = Be_Vietnam_Pro({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-sans",
  weight: ["400", "500", "600", "700"],
});

const fontSerif = Wittgenstein({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-serif",
});

const fontMono = Roboto_Mono({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "ZenSpa Platform",
  description: "Hệ thống chăm sóc khách hàng trực tuyến cho Spa",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi">
      <body
        className={`${fontSans.variable} ${fontSerif.variable} ${fontMono.variable} antialiased`}
      >
        {children}
        <Toaster position="bottom-right" richColors closeButton />
      </body>
    </html>
  );
}
