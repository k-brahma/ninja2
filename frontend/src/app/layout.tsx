import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'ブログアプリ',
  description: 'Django Ninja APIを使用したブログアプリケーション',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className={inter.className}>
        <Providers>
          <header className="bg-primary text-white p-4">
            <div className="container mx-auto flex justify-between items-center">
              <h1 className="text-2xl font-bold">ブログアプリ</h1>
              <nav>
                <ul className="flex space-x-4">
                  <li><a href="/" className="hover:underline">ホーム</a></li>
                  <li><a href="/login" className="hover:underline">ログイン</a></li>
                </ul>
              </nav>
            </div>
          </header>
          <main className="container mx-auto py-8 px-4">
            {children}
          </main>
          <footer className="bg-gray-800 text-white p-4 mt-8">
            <div className="container mx-auto text-center">
              <p>&copy; {new Date().getFullYear()} ブログアプリ</p>
            </div>
          </footer>
        </Providers>
      </body>
    </html>
  );
} 