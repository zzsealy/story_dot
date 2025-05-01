import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const nextConfig: NextConfig = {
  /* config options here */
  // basePath: '/quiz', // 强制所有路由添加前缀
  // async redirects() { // 可选：根路径重定向
  // return [
  //   {
  //     source: '/',
  //     destination: '/quiz',
  //     basePath: false,
  //     permanent: false
  //   }
  // ]
  // },
  images: {
    domains: [process.env.domain || "127.0.0.1"],
  },
  // i18n: {
  //   locales: ["en", "zh-CN"],
  //   defaultLocale: "zh-CN",
  // },
};
const withNextIntl = createNextIntlPlugin();
export default withNextIntl(nextConfig);
