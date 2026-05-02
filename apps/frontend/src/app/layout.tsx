import type { Metadata } from 'next'
import { Inter, Space_Grotesk, JetBrains_Mono } from 'next/font/google'
import '@/styles/globals.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-display',
  display: 'swap',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Eco-Shift | AI-Powered Supply Chain Orchestrator',
  description: 'Multi-agent supply chain orchestrator for sustainable logistics and emissions tracking',
  keywords: ['supply chain', 'sustainability', 'AI', 'emissions tracking', 'logistics'],
  authors: [{ name: 'Eco-Shift Team' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#22c55e',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html 
      lang="en" 
      className={`${inter.variable} ${spaceGrotesk.variable} ${jetbrainsMono.variable}`}
    >
      <body className="min-h-screen bg-neutral-50 font-sans antialiased">
        {/* Background Pattern */}
        <div className="fixed inset-0 bg-grid bg-noise pointer-events-none" aria-hidden="true" />
        
        {/* Main Content */}
        <div className="relative z-10">
          {children}
        </div>
      </body>
    </html>
  )
}

// Made with Bob
