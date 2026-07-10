import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "CivilOS Alpha 0.1",
  description: "AI-native civilization operating dashboard",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
