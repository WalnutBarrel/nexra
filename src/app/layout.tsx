import type { Metadata } from "next";
import { Outfit, Fira_Code } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";
import { TopNav } from "@/components/TopNav";

const outfit = Outfit({
  variable: "--font-inter", // keeping the css variable name same to avoid rewriting css unnecessarily
  subsets: ["latin"],
});

const firaCode = Fira_Code({
  variable: "--font-jetbrains-mono", // keeping the css variable name same
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
        className={`${outfit.variable} ${firaCode.variable} antialiased bg-background text-foreground`}
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

