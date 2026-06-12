from flask import Flask, render_template, request, redirect
import markdown
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("blog.db")
    conn.row_factory = sqlite3.Row
    return conn

# トップページ（記事一覧）
@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT id, title FROM posts").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

# 記事ページ
@app.route("/admin/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = get_db_connection()
        conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("new_post.html")

@app.route("/admin/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?",
                     (title, content, post_id))
        conn.commit()
        conn.close()

        return redirect(f"/post/{post_id}")

    conn.close()
    return render_template("edit_post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)
