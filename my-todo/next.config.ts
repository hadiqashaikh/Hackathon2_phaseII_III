import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  // Proxy API requests to Python backend during local development
  // EXCEPT /api/auth/* which is handled by Next.js (Better Auth)
  async rewrites() {
    return [
      {
        source: '/api/chat/:path*',
        destination: 'http://127.0.0.1:8000/api/chat/:path*',
      },
      {
        source: '/api/tasks/:path*',
        destination: 'http://127.0.0.1:8000/api/tasks/:path*',
      },
      {
        source: '/api/quick-tasks/:path*',
        destination: 'http://127.0.0.1:8000/api/quick-tasks/:path*',
      },
      {
        source: '/api/auth/me',
        destination: 'http://127.0.0.1:8000/api/auth/me',
      },
    ];
  },
  // Output configuration for Vercel deployment
  output: 'standalone',
};

export default nextConfig;
