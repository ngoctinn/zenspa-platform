import Footer from "@/components/common/footer";
import Navbar from "@/components/common/navbar";

export default function PublicLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      {/* Main Content */}
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}
