
１．リポジトリをダウンロード（またはクローン）
　git clone https://github.com/あなたの名前/リポジトリ名.git
　cd リポジトリ名

 2. 必要なパッケージをインストール
　Python が入っていれば OK です。
　pip install flask markdown

3. データベース（blog.db）を作成
　初回だけ、次のコマンドで SQLite のテーブルを作ります。
　pythonを起動

 import sqlite3
 conn = sqlite3.connect("blog.db")
 conn.execute("""
 CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    category TEXT
      )
  """)
 conn.commit()
 conn.close()

▶ アプリの起動方法
 python app.py

ブラウザで開きます： 
http://127.0.0.1:5000/

フォルダ構成（例）

project/
├── app.py
├── blog.db
├── templates/
│   ├── index.html
│   ├── post.html
│   ├── admin.html
│   ├── new_post.html
│   ├── edit_post.html
│   ├── categories.html
│   └── manage_categories.html
├── static/
│   └── style.css
└── README.md
