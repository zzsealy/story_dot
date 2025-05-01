// app/[locale]/layout.tsx
// 这是一个服务器组件，不需要 "use client";

import React from "react";
import { ReactNode } from "react";
// 注意：这里引入的全局样式只会在这个布局和它的子元素中生效
import "../globals.css"; // 引入全局样式 (相对于 app 目录)

import { Inter } from "next/font/google";
// 如果 Button, Link, Toaster 在布局或其子级客户端组件中使用，需要导入
import { Button } from "@/components/ui/button"; // 示例组件
import Link from "next/link"; // Next.js Link
import { Toaster } from "sonner"; // 第三方组件

// === next-intl 相关的导入 ===
import { getTranslations } from "next-intl/server"; // 用于在服务器组件中翻译

// === 导入语言切换客户端组件 ===
import LocaleSwitcher from "@/components/LocaleSwitcher";

const inter = Inter({ subsets: ["latin"] });

type Props = {
  children: ReactNode;
  params: { locale: string };
};

// 根布局 - 服务器组件 (SSR 会在这里发生)

import { NextIntlClientProvider, hasLocale } from "next-intl";
import { notFound } from "next/navigation";
import { routing } from "@/i18n/routing";

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  // Ensure that the incoming `locale` is valid
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) {
    notFound();
  }
  return (
    <html lang={locale}>
      <body>
        <Toaster position="top-right" />
        <header className="bg-white-800 text-teal-400">
          <nav className="container mx-auto flex items-center justify-between py-4 px-4">
            {/* Logo or Website Name */}
            <Link href="/" className="text-xl font-bold hover:text-gray-300">
              MyWebsite
            </Link>

            {/* Navigation Links */}
            <div className="flex items-center gap-4">
              <Link href="/about" className="hover:text-green-300">
                About
              </Link>
              <Link href="/services" className="hover:text-green-300">
                Services
              </Link>
              <Link href="/contact" className="hover:text-green-300">
                Contact
              </Link>

              {/* Action Button */}

              <Link href="/register">
                <Button className="bg-blue-500 hover:bg-blue-600 text-white">
                  注册
                </Button>
              </Link>
              <Link href="/login">
                <Button className="bg-blue-500 hover:bg-blue-600 text-white">
                  登录
                </Button>
              </Link>
            </div>
          </nav>
        </header>
        <NextIntlClientProvider>{children}</NextIntlClientProvider>
      </body>
    </html>
  );
}
