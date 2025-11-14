import Link from "next/link";

const Footer = () => {
  return (
    <footer className="border-t border-primary-foreground/20 bg-primary text-primary-foreground">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="font-semibold mb-4">ZenSpa</h3>
            <p className="text-sm text-primary-foreground/80">
              Hệ thống chăm sóc khách hàng trực tuyến cho Spa chuyên nghiệp.
            </p>
          </div>
          <div>
            <h4 className="font-medium mb-4">Dịch vụ</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link
                  href="#services"
                  className="hover:underline transition-all duration-200 ease-in-out"
                >
                  Chăm sóc da
                </Link>
              </li>
              <li>
                <Link
                  href="#services"
                  className="hover:underline transition-all duration-200 ease-in-out"
                >
                  Massage
                </Link>
              </li>
              <li>
                <Link
                  href="#services"
                  className="hover:underline transition-all duration-200 ease-in-out"
                >
                  Gội đầu
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium mb-4">Liên hệ</h4>
            <ul className="space-y-2 text-sm text-primary-foreground/80">
              <li>Địa chỉ: 123 Đường Spa, TP.HCM</li>
              <li>Điện thoại: 0123 456 789</li>
              <li>Email: info@zenspa.vn</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium mb-4">Giờ mở cửa</h4>
            <ul className="space-y-2 text-sm text-primary-foreground/80">
              <li>Thứ 2 - Thứ 6: 8:00 - 20:00</li>
              <li>Thứ 7 - Chủ nhật: 9:00 - 18:00</li>
            </ul>
          </div>
        </div>
        <div className="border-t border-primary-foreground/20 mt-8 pt-8 text-center text-sm">
          <p>&copy; 2025 ZenSpa. Tất cả quyền được bảo lưu.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
