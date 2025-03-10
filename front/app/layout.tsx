'use client';
import React from 'react';
import './globals.css';  // 引入全局样式
import { Inter } from 'next/font/google';
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Toaster } from 'sonner';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
     <html lang="en">
    <body className={inter.className}>
      <Toaster position='top-right' />
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
        {children}
    </body>
  </html>
  );
}

