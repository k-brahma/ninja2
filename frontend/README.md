# ブログアプリケーション フロントエンド

このプロジェクトは、React (Next.js) で構築されたブログアプリケーションのフロントエンドです。バックエンドとしてDjango + Django Ninjaを使用しています。

## 機能

- ユーザー認証（ログイン、ログアウト）
- ブログ記事の一覧表示
- ブログ記事の詳細表示
- 記事の作成、編集、削除（認証済みユーザーのみ）

## 使用技術

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios（APIリクエスト用）

## 始め方

### 依存関係のインストール

```bash
npm install
```

### 開発サーバーの起動

```bash
npm run dev
```

これで開発サーバーがポート3000で起動します（http://localhost:3000）。

## API接続

このフロントエンドは、ポート8000で実行されているDjango Ninjaバックエンドと通信するように設定されています。`next.config.mjs`ファイルのrewrites設定によって、`/api/*`へのリクエストがバックエンドサーバーにプロキシされます。

## プロジェクト構造

```
frontend/
├── src/                # ソースコード
│   ├── app/            # Next.js App Router
│   │   ├── login/      # ログインページ
│   │   ├── posts/      # 記事関連ページ
│   │   ├── globals.css # グローバルスタイル
│   │   ├── layout.tsx  # レイアウトコンポーネント
│   │   ├── page.tsx    # ホームページ
│   │   └── providers.tsx # コンテクストプロバイダー
│   ├── components/     # 再利用可能なコンポーネント
│   └── lib/            # ユーティリティ、ヘルパー関数
│       ├── api.ts      # APIクライアント
│       └── AuthContext.tsx # 認証コンテキスト
├── public/             # 静的ファイル
├── next.config.mjs     # Next.js設定
├── package.json        # 依存関係
└── tsconfig.json       # TypeScript設定
```

## 本番環境へのデプロイ

ビルドを作成するには:

```bash
npm run build
```

ビルドされたアプリケーションを起動するには:

```bash
npm run start
``` 