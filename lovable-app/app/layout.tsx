import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Zenthral - AI Automation',
  description: 'AI automation without installation',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
