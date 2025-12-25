/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        domains: ['s1.ticketm.net', 'img.evbuc.com'],
    },
    output: 'standalone',
    typescript: {
        ignoreBuildErrors: true,
    },
    eslint: {
        ignoreDuringBuilds: true,
    },
}

module.exports = nextConfig
