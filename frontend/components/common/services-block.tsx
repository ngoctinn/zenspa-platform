import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const services = [
  {
    title: "Massage Thư Giãn",
    description:
      "Trải nghiệm massage chuyên nghiệp giúp thư giãn cơ thể và tinh thần.",
    icon: "🧘",
  },
  {
    title: "Chăm Sóc Da",
    description: "Dịch vụ chăm sóc da chuyên sâu với công nghệ tiên tiến.",
    icon: "💆",
  },
  {
    title: "Liệu Trình Spa",
    description: "Các liệu trình spa toàn diện cho sức khỏe và vẻ đẹp.",
    icon: "🌿",
  },
  {
    title: "Tư Vấn Cá Nhân",
    description: "Tư vấn viên chuyên nghiệp hỗ trợ lựa chọn dịch vụ phù hợp.",
    icon: "💬",
  },
];

export default function ServicesBlock() {
  return (
    <section className="py-16 bg-muted/50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <Badge variant="secondary" className="mb-4">
            Dịch Vụ Của Chúng Tôi
          </Badge>
          <h2 className="text-3xl font-bold mb-4">
            Trải Nghiệm Spa Chuyên Nghiệp
            <svg
              className="inline-block ml-2 w-8 h-2"
              viewBox="0 0 32 8"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M1 4C8 1 16 7 24 4C32 1 40 7 48 4"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Chúng tôi cung cấp các dịch vụ spa chất lượng cao, được thiết kế để
            mang lại sự thư giãn và chăm sóc tối ưu cho khách hàng.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {services.map((service, index) => (
            <Card
              key={index}
              className="text-center hover:shadow-lg transition-shadow"
            >
              <CardHeader>
                <div className="text-4xl mb-4">{service.icon}</div>
                <CardTitle className="text-xl">{service.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>{service.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
