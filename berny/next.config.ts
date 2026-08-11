import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  allowedDevOrigins: ['localhost', '172.18.0.1', '172.18.0.1', '192.168.31.110', '192.168.56.1'],
  turbopack: {},
};

export default nextConfig;