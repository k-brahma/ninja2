'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { blogApi } from '@/lib/api';
import { useAuth } from '@/lib/AuthContext';

interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  author: {
    id: number;
    username: string;
  };
}

export default function PostPage() {
  const params = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const postId = Number(params.id);
    if (isNaN(postId)) {
      setError('無効な記事IDです');
      setLoading(false);
      return;
    }

    const fetchPost = async () => {
      try {
        const data = await blogApi.getPost(postId);
        setPost(data);
      } catch (err) {
        setError('記事の取得に失敗しました');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [params.id]);

  const handleDelete = async () => {
    if (!post) return;
    
    if (!confirm('本当にこの記事を削除しますか？')) {
      return;
    }
    
    try {
      await blogApi.deletePost(post.id);
      router.push('/');
    } catch (err) {
      console.error('Failed to delete post:', err);
      alert('記事の削除に失敗しました');
    }
  };

  if (loading) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-500">読み込み中...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 p-4 rounded my-6">
        <p className="text-red-700">{error}</p>
        <button 
          onClick={() => router.push('/')} 
          className="mt-4 bg-primary text-white px-4 py-2 rounded"
        >
          ホームへ戻る
        </button>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-500">記事が見つかりませんでした</p>
        <button 
          onClick={() => router.push('/')} 
          className="mt-4 bg-primary text-white px-4 py-2 rounded"
        >
          ホームへ戻る
        </button>
      </div>
    );
  }

  const isAuthor = user && post.author.id === user.id;

  return (
    <article className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">{post.title}</h1>
      <div className="flex justify-between items-center text-gray-500 mb-8">
        <span>著者: {post.author.username}</span>
        <span>{new Date(post.created_at).toLocaleDateString('ja-JP')}</span>
      </div>
      
      <div className="prose lg:prose-xl mb-8">
        {post.content.split('\n').map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
      
      {isAuthor && (
        <div className="flex space-x-4 mt-8">
          <button 
            onClick={() => router.push(`/posts/${post.id}/edit`)} 
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            編集
          </button>
          <button 
            onClick={handleDelete} 
            className="bg-red-500 text-white px-4 py-2 rounded"
          >
            削除
          </button>
        </div>
      )}
      
      <button 
        onClick={() => router.push('/')} 
        className="mt-8 text-primary hover:underline flex items-center"
      >
        ← 記事一覧に戻る
      </button>
    </article>
  );
} 