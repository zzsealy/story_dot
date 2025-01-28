import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: {
    domains: [process.env.domain || '127.0.0.1']
  }
};

export default nextConfig;
