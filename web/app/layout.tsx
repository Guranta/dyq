import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "大云雀",
  description: "AI 视频、图片与短剧创作平台",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh-CN">
      <body>
        <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
          <Link href="/" className="text-xl font-semibold tracking-tight">
            大云雀
          </Link>
          <nav className="flex items-center gap-4 text-sm text-slate-300">
            <Link className="hover:text-white" href="/create/image">
              图片创作
            </Link>
            <Link className="hover:text-white" href="/create/video">
              视频创作
            </Link>
          </nav>
        </header>
        {children}
      </body>
    </html>
  );
}
