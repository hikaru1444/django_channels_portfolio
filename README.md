## 作成日: 2023年4月6日


# 公開先


https://github.com/hikaru1444/djangochannels



# 概要


Python,Djangoの強力な機能を持ち合わせている同時編集可能なスプレッドシートアプリとなっています。

urls.pyに1行追加するだけでdjango.contrib.adminのような使用感でモデルを編集することができます｡


```
path("room/", views.RoomView.as_view(model=Shop), name="room")  # 例
```



# サンプル


編集をするともう片方のウィンドウにも反映されること、ページの更新をしてモデルが保存されていることを確認しています。


https://github.com/hikaru1444/djangochannels/assets/82006837/31b2f2ad-d9b7-45c2-b60a-5b0e36ea2109




# インストール


## Python3,PostgreSQLをインストール


## Git

```
git clone https://github.com/hikaru1444/djangochannels
```

## Docker


Dockerのダウンロード先 https://www.docker.com/products/docker-desktop/
```
$ docker run --rm -p 6379:6379 redis:7
```


## Django


```
cd djangochannels

.\.venv\Scripts\activate

pip install -V requirements.txt
```

.envにPostgreSQLの設定をする

```
python manage.py migrations

python manage.py runserver
```

http://127.0.0.1:8000

にアクセスして編集が出来れば成功

※ migrationsで初期データを100件生成している


## 追記
2024年11月6日
chat/views.pyにあるzoomを変更するとセル幅の自動調整がうまくいかなくなります
例: zoom=0.8に設定してrunserverした後に金額列に「123456789」と入力すると「89」が見切れて表示される
zoomを使うのはスプレットシートが大きい時が多いためstrechHを使いといいかもしれません
例: chat/views.pyのhot_settingsに「'stretchH': 'all',」を追加
