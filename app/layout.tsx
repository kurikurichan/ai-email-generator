import "./globals.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });
import Sidebar from "./components/sidebar";
import Header from "./components/header";

export const metadata = {
  title: "Client Lead Email Generator",
  description: "Created by Krista Strucke",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Header />
        <main className="flex min-h-screen bg-fixed bg-cover bg-spacebg">
          <Sidebar />
          {children}
        </main>
      </body>
    </html>
  );
}
