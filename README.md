# 勉強時間管理アプリ

勉強時間の管理・可視化を行う Django アプリです。

## 使い方

1. 必要パッケージをインストールします。

   ```sh
   poetry install
   ```

1. secret key を生成します。

   ```sh
   poetry run python studyvisapp/utils.py >| studyvis/local_settings.py
   ```

1. `sample.config.yaml`をコピーして、`config.yaml`にリネームします。作成した`config.yaml`において、勉強項目と表示色を登録します。色の名前は[Bootstrap ドキュメント](https://getbootstrap.jp/docs/4.4/utilities/colors/)をご参照ください。

1. モデルをデータベースに反映させます。

   ```sh
   poetry run python manage.py makemigrations
   poetry run python manage.py migrate
   ```

1. サーバーを起動します。

   ```sh
   poetry run python manage.py runserver
   ```

## 画面

https://user-images.githubusercontent.com/50258785/129472563-366180f6-739d-4906-b004-14cdc12025e0.mp4
