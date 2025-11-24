"use client";

import { Button } from "@/components/ui/button";
import Image from "next/image";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";

const HeroSection = () => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.1 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <section className="relative w-full pt-8 pb-12 lg:pt-12 lg:pb-20 bg-background overflow-hidden">
      <div className="container px-4 md:px-6 mx-auto">
        <div className="grid gap-12 lg:grid-cols-2 lg:gap-16 items-center">
          {/* Left Content */}
          <div className="flex flex-col justify-center space-y-8 animate-in fade-in slide-in-from-left-8 duration-500 fill-mode-both  lg:-mt-30">
            <div className="space-y-4">
              <h1 className="text-4xl font-extrabold tracking-tighter sm:text-3xl md:text-4xl lg:text-4xl/none">
                <span className="text-primary">Tinh tế</span>{" "}
                <span className="text-primary">-</span>{" "}
                <span className="text-thirdary ">Riêng tư</span>{" "}
                <span className="text-thirdary ">-</span>{" "}
                <span className="text-quaternary ">Thư giãn</span>
              </h1>
              <p className="max-w-[600px] text-muted-foreground md:text-2xl leading-relaxed">
                Kết hợp tinh tế giữa kỹ thuật trị liệu truyền thống và công nghệ
                chăm sóc da hiện đại. Chúng tôi mang đến lộ trình chuyên sâu
                giúp bạn phục hồi cơ thể, tái tạo năng lượng và tìm lại sự cân
                bằng.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <Button
                size="lg"
                className="h-12 px-8 rounded-full text-base shadow-md hover:scale-105"
                asChild
              >
                <Link href="/booking">Đặt Lịch Ngay</Link>
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="h-12 px-8 rounded-full text-base border-2 border-primary/20 text-primary hover:bg-primary/5 hover:border-primary hover:scale-105"
                asChild
              >
                <Link href="#services">Xem Dịch Vụ</Link>
              </Button>
            </div>
          </div>

          {/* Right Images - Masonry Grid Layout */}
          <div
            ref={ref}
            className={`relative grid grid-cols-2 gap-6 transition-all duration-1000 ease-out ${
              isVisible
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-10"
            }`}
          >
            {/* Fade Overlay Top */}
            <div className="absolute -top-4 left-0 right-0 h-32 bg-gradient-to-b from-background via-background/90 to-transparent z-20 pointer-events-none" />

            {/* Fade Overlay Bottom */}
            <div className="absolute -bottom-4 left-0 right-0 h-32 bg-gradient-to-t from-background via-background/90 to-transparent z-20 pointer-events-none" />

            {/* Column 1 */}
            <div className="grid gap-6">
              <div className="relative h-[160px] sm:h-[200px] rounded-2xl overflow-hidden shadow-lg">
                <Image
                  src="https://i.pinimg.com/736x/f0/d2/77/f0d2774f08cee3574f17049b68b599d7.jpg"
                  alt="Spa ambiance"
                  fill
                  className="object-cover hover:scale-105 transition-transform duration-700"
                />
              </div>
              <div className="relative h-[200px] sm:h-[260px] rounded-2xl overflow-hidden shadow-lg">
                <Image
                  src="https://i.pinimg.com/736x/9f/3e/98/9f3e987e49a27f81f04e02a7c6bc9f16.jpg"
                  alt="Spa treatment"
                  fill
                  className="object-cover hover:scale-105 transition-transform duration-700"
                />
              </div>
              <div className="relative h-[140px] sm:h-[180px] rounded-2xl overflow-hidden shadow-lg">
                <Image
                  src="https://i.pinimg.com/736x/f0/d2/77/f0d2774f08cee3574f17049b68b599d7.jpg"
                  alt="Spa detail"
                  fill
                  className="object-cover hover:scale-105 transition-transform duration-700"
                />
              </div>
            </div>

            {/* Column 2 */}
            <div className="grid gap-6 pt-12 sm:pt-16">
              <div className="relative h-[260px] sm:h-[320px] rounded-2xl overflow-hidden shadow-lg">
                <Image
                  src="https://i.pinimg.com/736x/9f/3e/98/9f3e987e49a27f81f04e02a7c6bc9f16.jpg"
                  alt="Facial treatment"
                  fill
                  className="object-cover hover:scale-105 transition-transform duration-700"
                />
              </div>
              <div className="relative h-[160px] sm:h-[200px] rounded-2xl overflow-hidden shadow-lg">
                <Image
                  src="https://i.pinimg.com/736x/f0/d2/77/f0d2774f08cee3574f17049b68b599d7.jpg"
                  alt="Relaxing environment"
                  fill
                  className="object-cover hover:scale-105 transition-transform duration-700"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
