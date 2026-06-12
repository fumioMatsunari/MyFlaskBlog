import sqlite3

conn = sqlite3.connect("blog.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
""")

# サンプル記事を追加
c.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
          ("今日のパソコン勉強", "# Flask を勉強しました\n\nMarkdown も使えるようになりました。"))

c.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
          ("日常のあれこれ", "## 今日の散歩\n\n公園を歩きました。"))

conn.commit()
conn.close()

print("データベースを作成しました。")
