"use client";

import { Button } from "@/components/ui/button";
import Image from "next/image";
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
    <section className="min-h-[80vh] flex items-center bg-gradient-to-r from-background via-background to-muted/20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-6 animate-in fade-in slide-in-from-left-4 duration-1000">
            {/* Headline */}
            <h1 className="text-3xl lg:text-5xl font-extrabold leading-tight text-primary">
              Chăm Sóc Toàn Diện,
              <br />
              <span className="text-primary">
                Đánh Thức Vẻ Đẹp Tiềm Ẩn Của Bạn
              </span>
            </h1>

            {/* Sub-description */}
            <p className="text-lg text-slate-600 max-w-lg">
              Trải nghiệm các liệu pháp Spa cao cấp từ thư giãn cơ thể đến chăm
              sóc da chuyên sâu. Đội ngũ chuyên gia tận tâm, không gian yên bình
              sẽ mang đến cho bạn những khoảnh khắc tuyệt vời nhất.
            </p>

            {/* CTA */}
            <Button
              size="lg"
              className="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold px-10 py-4 text-lg shadow-lg hover:shadow-xl transition-all duration-300 animate-bounce"
            >
              Đặt Lịch Ngay!
            </Button>
          </div>

          {/* Right Images - Mosaic Grid Layout */}
          <div
            ref={ref}
            className={`flex gap-3 transition-opacity duration-1000 ${
              isVisible ? "opacity-100" : "opacity-0"
            }`}
          >
            {/* Ảnh 1: Không gian (Chủ đạo - Vertical) */}
            <div className="flex-1">
              <Image
                width={400}
                height={600}
                src="https://i.pinimg.com/736x/f0/d2/77/f0d2774f08cee3574f17049b68b599d7.jpg"
                alt="Spa ambiance"
                className="w-full h-full object-cover rounded-lg shadow-lg animate-in fade-in transition-all duration-300 hover:scale-103"
              />
            </div>
            {/* Right Column: Ảnh 2 và 3 */}
            <div className="flex flex-col gap-3">
              {/* Ảnh 2: Liệu trình (Square) */}
              <Image
                width={200}
                height={200}
                src="https://i.pinimg.com/736x/9f/3e/98/9f3e987e49a27f81f04e02a7c6bc9f16.jpg"
                alt="Spa treatment"
                className="w-full h-full object-cover rounded-lg shadow-lg animate-in fade-in delay-100 transition-all duration-300 hover:scale-103"
              />
              {/* Ảnh 3: Chi tiết (Square) */}
              <Image
                width={200}
                height={200}
                src="https://i.pinimg.com/736x/f0/d2/77/f0d2774f08cee3574f17049b68b599d7.jpg"
                alt="Spa detail"
                className="w-full h-full object-cover rounded-lg shadow-lg animate-in fade-in delay-200 transition-all duration-300 hover:scale-103"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
