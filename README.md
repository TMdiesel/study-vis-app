# 勉強時間管理アプリ

勉強時間の管理・可視化を行う Django アプリです。

## 使い方

1. 必要パッケージをインストールします。

   ```sh
   poetry install
   ```

1. モデルをデータベースに反映させます。

   ```sh
   poetry run python manage.py makemigrations
   poetry run python manage.py migrate
   ```

1. サーバーを起動します。

   ```sh
   poetry run python manage.py runserver
   ```
