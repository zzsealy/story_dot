'use client';
import React from 'react';
import './globals.css';  // 引入全局样式
import { Inter } from 'next/font/google';
// import Link from 'next/link';

const inter = Inter({ subsets: ['latin'] });
import { AntdRegistry } from '@ant-design/nextjs-registry'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
     <html lang="en">
    <body className={inter.className}>
      <AntdRegistry>
        {children}
      </AntdRegistry>
    </body>
  </html>
  );
}

