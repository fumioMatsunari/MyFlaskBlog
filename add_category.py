import sqlite3

conn = sqlite3.connect("blog.db")
conn.execute("ALTER TABLE posts ADD COLUMN category TEXT;")
conn.commit()
conn.close()

print("category カラムを追加しました！")
