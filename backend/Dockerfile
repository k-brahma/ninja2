FROM python:3.11-slim

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係のインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . /app/

# ポートを公開
EXPOSE 8000

# 実行コマンド
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"] 