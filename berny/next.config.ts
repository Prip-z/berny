import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  allowedDevOrigins: ['localhost:3000', '172.18.0.1:3000', '172.18.0.1', '192.168.56.1'],
  turbopack: {},
};

export default nextConfig;