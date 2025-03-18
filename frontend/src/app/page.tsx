"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface BlogPost {
  id: number;
  title: string;
  content: string;
  created_at: string;
  author: {
    id: number;
    username: string;
  };
}

export default function Home() {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch('/api/blog/posts/');
        if (!response.ok) {
          throw new Error('Failed to fetch posts');
        }
        const data = await response.json();
        setPosts(data);
      } catch (err) {
        setError('記事の取得に失敗しました。');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">最新の記事</h1>
      
      {loading && (
        <div className="text-center py-10">
          <p className="text-gray-500">読み込み中...</p>
        </div>
      )}
      
      {error && (
        <div className="bg-red-100 p-4 rounded mb-6">
          <p className="text-red-700">{error}</p>
        </div>
      )}
      
      {!loading && !error && posts.length === 0 && (
        <div className="text-center py-10">
          <p className="text-gray-500">記事がありません。</p>
        </div>
      )}
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {posts.map((post) => (
          <div key={post.id} className="border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition">
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-2">{post.title}</h2>
              <p className="text-gray-600 mb-4">
                {post.content.substring(0, 100)}
                {post.content.length > 100 ? '...' : ''}
              </p>
              <div className="flex justify-between items-center text-sm text-gray-500">
                <span>投稿者: {post.author.username}</span>
                <span>{new Date(post.created_at).toLocaleDateString('ja-JP')}</span>
              </div>
              <Link href={`/posts/${post.id}`} className="mt-4 inline-block bg-primary text-white px-4 py-2 rounded hover:bg-blue-600 transition">
                続きを読む
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
} 