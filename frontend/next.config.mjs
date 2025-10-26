/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  i18n: {
    locales: ['vi'],
    defaultLocale: 'vi'
  }
};

export default nextConfig;
