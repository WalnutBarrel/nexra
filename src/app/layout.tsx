import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";
import { TopNav } from "@/components/TopNav";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Nexra | Intelligence Platform",
  description: "A premium, calm, and dense intelligence platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${inter.variable} ${jetbrainsMono.variable} antialiased bg-background text-foreground`}
      >
        <Sidebar />
        <div className="pl-64 flex flex-col min-h-screen">
          <TopNav />
          <main className="flex-1 overflow-x-hidden">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}

