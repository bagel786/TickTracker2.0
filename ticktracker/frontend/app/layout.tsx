import type { Metadata } from 'next'
import Script from 'next/script'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'TickTracker',
    description: 'AI-Powered Ticket Price Forecasting',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <Script
                    src="https://www.googletagmanager.com/gtag/js?id=G-VBWWR89NJW"
                    strategy="afterInteractive"
                />
                <Script id="google-analytics" strategy="afterInteractive">
                    {`
                        window.dataLayer = window.dataLayer || [];
                        function gtag(){dataLayer.push(arguments);}
                        gtag('js', new Date());

                        gtag('config', 'G-VBWWR89NJW');
                    `}
                </Script>
                <main className="min-h-screen flex flex-col">
                    {children}
                </main>
            </body>
        </html>
    )
}
