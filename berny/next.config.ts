import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  allowedDevOrigins: ['localhost:3000', '172.18.0.1:3000', '172.18.0.1', '192.168.31.110'],
  turbopack: {},
};

export default nextConfig;