import { join } from "path";

/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack(config) {
    // Alias '@/' to point to the 'src' folder
    config.resolve.alias['@'] = join(__dirname, 'src');
    return config;
  },
};

export default nextConfig;
