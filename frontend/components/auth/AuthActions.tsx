import { Button } from "@/components/ui/button";
import Link from "next/link";

const AuthActions = () => {
  return (
    <div className="flex items-center space-x-4">
      <Link
        href="/signin"
        className="text-primary-foreground hover:underline transition-all duration-200 ease-in-out"
      >
        Đăng nhập
      </Link>
      <Button className="bg-white text-primary hover:bg-white/90" asChild>
        <Link href="/signup">Đăng ký</Link>
      </Button>
    </div>
  );
};

export default AuthActions;
