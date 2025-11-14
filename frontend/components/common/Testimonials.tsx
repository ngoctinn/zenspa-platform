import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

const testimonials = [
  {
    name: "Nguyễn Thị A",
    role: "Khách hàng thân thiết",
    quote:
      "Dịch vụ tại ZenSpa thật tuyệt vời! Tôi cảm thấy rất thư giãn sau mỗi lần đến đây.",
    avatar: "NA",
  },
  {
    name: "Trần Văn B",
    role: "Khách hàng VIP",
    quote:
      "Nhân viên chuyên nghiệp, không gian sang trọng. Tôi sẽ quay lại lần nữa!",
    avatar: "TB",
  },
  {
    name: "Lê Thị C",
    role: "Khách hàng mới",
    quote: "Trải nghiệm massage ở đây là tốt nhất tôi từng có. Rất hài lòng!",
    avatar: "LC",
  },
];

export default function Testimonials() {
  return (
    <section className="py-16 bg-background">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <Badge variant="secondary" className="mb-4">
            Phản Hồi Từ Khách Hàng
          </Badge>
          <h2 className="text-3xl font-bold mb-4">
            Những Ý Kiến Từ Khách Hàng
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
            Hãy nghe những gì khách hàng của chúng tôi nói về trải nghiệm tại
            ZenSpa.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardContent className="pt-6">
                <div className="flex items-center mb-4">
                  <Avatar className="mr-4">
                    <AvatarFallback>{testimonial.avatar}</AvatarFallback>
                  </Avatar>
                  <div>
                    <h3 className="font-semibold">{testimonial.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      {testimonial.role}
                    </p>
                  </div>
                </div>
                <p className="text-muted-foreground italic">
                  &ldquo;{testimonial.quote}&rdquo;
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
