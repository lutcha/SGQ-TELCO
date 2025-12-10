import type { Metadata } from "next";
import "./globals.css";
import { ReactQueryProvider } from "../components/providers/ReactQueryProvider";

export const metadata: Metadata = {
  title: "SGQ Telco - Auditorias",
  description: "Gestão integrada de auditorias ISO 9001"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt">
      <body className="bg-slate-50 text-slate-900">
        <ReactQueryProvider>{children}</ReactQueryProvider>
      </body>
    </html>
  );
}
