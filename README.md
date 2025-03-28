# Django Ninja ブログAPI

UUIDをIDとして使用するカスタムユーザーモデルを実装したDjango Ninjaベースのブログ＆認証APIです。

## 機能

- カスタムユーザー認証 (UUIDベース)
- JWT認証
- OAuth2プロバイダー
- ブログ記事とコメント管理
- OpenAPI (Swagger UI) ドキュメント

## 環境構築

このプロジェクトは以下の2つの方法で実行できます：

1. ローカル開発環境（venv + SQLite）
2. Docker環境（PostgreSQL使用）

### 初期設定

#### 環境変数の設定

```bash
# ルートディレクトリで.envファイルを作成
cp .env.sample .env
# 必要に応じて.envの内容を編集

# Docker用の環境変数（Dockerを使用する場合）
cp docker/.env.sample docker/.env
# 必要に応じてdocker/.envの内容を編集
```

`.env_sample`ファイルを基に`.env`を作成する際は、セキュリティのために必ず以下の項目を変更してください：

1. **SECRET_KEY** - Djangoの秘密鍵（以下のコマンドで生成できます）
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. データベースパスワード - 本番環境では必ず強力なパスワードに変更してください
3. その他、メール設定やOAuth関連の認証情報など、必要に応じて設定してください

本番環境では`DEBUG=False`に設定し、`ALLOWED_HOSTS`に実際のドメイン名を設定することをお忘れなく。

## ローカル開発環境での実行方法

### 1. 仮想環境の作成とアクティベート

```bash
cd backend
python -m venv venv

# Windowsの場合
venv\Scripts\activate

# macOS/Linuxの場合
source venv/bin/activate
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. 構成チェック

```bash
python manage.py check
```

### 4. データベースのマイグレーション

```bash
python manage.py migrate
```

### 5. 開発サーバーの起動

```bash
python manage.py runserver
```

サーバーが起動したら、ブラウザで http://127.0.0.1:8000/api/docs にアクセスしてSwagger UIを表示できます。

## Docker環境での実行方法

### 1. Dockerとdocker-composeのインストール

お使いのOSに合わせてDockerとdocker-composeをインストールしてください。

### 2. コンテナのビルドと起動

```bash
cd docker
docker-compose up --build
```

初回は依存パッケージのインストールとデータベースの構築に時間がかかります。

### 3. バックグラウンドでの実行（オプション）

```bash
docker-compose up -d
```

### 4. コンテナの停止

```bash
docker-compose down
```

Dockerを使用する場合、サーバーは http://localhost:8000/api/docs でアクセスできます。

## APIエンドポイント

APIは以下のエンドポイントで利用可能です：

### 認証

- `POST /api/auth/register` - 新規ユーザー登録
- `POST /api/auth/login` - ログイン（JWTトークン取得）
- `POST /api/auth/logout` - ログアウト
- `GET /api/auth/me` - 現在のユーザー情報取得

### ブログ

- `GET /api/blog/` - ブログ記事一覧
- `POST /api/blog/` - ブログ記事作成
- `GET /api/blog/{entry_id}` - ブログ記事詳細
- `PUT /api/blog/{entry_id}` - ブログ記事更新
- `DELETE /api/blog/{entry_id}` - ブログ記事削除

### コメント

- `GET /api/blog/{blog_id}/comments/` - コメント一覧
- `POST /api/blog/{blog_id}/comments/` - コメント作成
- `PUT /api/blog/{blog_id}/comments/{comment_id}` - コメント更新
- `DELETE /api/blog/{blog_id}/comments/{comment_id}` - コメント削除

## OAuth2の設定（オプション）

OAuth2プロバイダーとしてのテストを行う場合：

1. ngrokをインストールして実行：
```bash
ngrok http 8000
```

2. 表示されたngrokのURLをDjangoのALLOWED_HOSTSに追加
3. OAuth2クライアントを登録：
```bash
python manage.py createsuperuser
# 管理画面（/admin/）にアクセスしてOAuth2クライアントを設定
``` 