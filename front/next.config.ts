import type { NextConfig } from "next";

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
    domains: [process.env.domain || '127.0.0.1']
  }
};

export default nextConfig;
