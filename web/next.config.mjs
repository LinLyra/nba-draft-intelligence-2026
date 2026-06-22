/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "cdn.nba.com" },
      { protocol: "https", hostname: "a.espncdn.com" },
      { protocol: "https", hostname: "d2uki2uvp6v3wr.cloudfront.net" },
    ],
  },
};

export default nextConfig;
