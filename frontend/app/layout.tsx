import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Tra cứu HS Code Hải quan Việt Nam",
  description: "Nền tảng tra cứu kết quả phân tích phân loại và mã HS cập nhật",
  keywords: ["HS code", "Hải quan", "phân tích phân loại", "Việt Nam"],
  openGraph: {
    title: "Tra cứu HS Code Hải quan Việt Nam",
    description: "Thu thập và chuẩn hóa dữ liệu phân tích phân loại từ Tổng cục Hải quan",
    locale: "vi_VN",
    siteName: "HS Code Platform"
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body className="bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}
