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

# 記事追加ページ
@app.route("/admin/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]

        # ★ ここに追加する！
        new_category = request.form.get("new_category")
        if new_category:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO posts (title, content, category) VALUES (?, ?, ?)",
                ("(カテゴリー用)", "", new_category)
            )
            conn.commit()
            conn.close()
            category = new_category

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO posts (title, content, category) VALUES (?, ?, ?)",
            (title, content, category)
        )
        conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("new_post.html", categories=get_categories())


# 記事編集ページ
@app.route("/admin/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]

        # ★ ここに追加する！
        new_category = request.form.get("new_category")
        if new_category:
            conn.execute(
                "INSERT INTO posts (title, content, category) VALUES (?, ?, ?)",
                ("(カテゴリー用)", "", new_category)
            )
            conn.commit()
            category = new_category

        conn.execute(
            "UPDATE posts SET title = ?, content = ?, category = ? WHERE id = ?",
            (title, content, category, post_id)
        )
        conn.commit()
        conn.close()

        return redirect(f"/post/{post_id}")

    conn.close()
    return render_template("edit_post.html", post=post, categories=get_categories())


# 記事ページ
@app.route("/post/<int:post_id>")
def post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()

    html_content = markdown.markdown(post["content"])

    return render_template("post.html", post=post, html_content=html_content)

@app.route("/admin")
def admin():
    conn = get_db_connection()
    posts = conn.execute("SELECT id, title, category FROM posts").fetchall()
    count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    conn.close()
    return render_template("admin.html", posts=posts, count=count)


@app.route("/admin/delete/<int:post_id>")
def delete_post(post_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

@app.route("/category/<name>")
def category_page(name):
    conn = get_db_connection()
    posts = conn.execute(
        "SELECT id, title, category FROM posts WHERE category = ?",
        (name,)
    ).fetchall()
    conn.close()

    return render_template("category.html", posts=posts, category=name)

@app.route("/categories")
def categories():
    conn = get_db_connection()
    rows = conn.execute("SELECT DISTINCT category FROM posts WHERE category IS NOT NULL").fetchall()
    conn.close()

    categories = [row["category"] for row in rows]

    return render_template("categories.html", categories=categories)

def get_categories():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT DISTINCT category FROM posts WHERE category IS NOT NULL ORDER BY category ASC"
    ).fetchall()
    conn.close()
    return [row["category"] for row in rows]


@app.route("/admin/categories", methods=["GET", "POST"])
def manage_categories():
    conn = get_db_connection()

    # カテゴリー追加
    if request.method == "POST":
        new_cat = request.form["new_category"]
        if new_cat:
            # ダミー記事を追加してカテゴリーを登録
            conn.execute(
                "INSERT INTO posts (title, content, category) VALUES (?, ?, ?)",
                ("(カテゴリー用)", "", new_cat)
            )
            conn.commit()

    # カテゴリー一覧取得
    rows = conn.execute(
        "SELECT DISTINCT category FROM posts WHERE category IS NOT NULL"
    ).fetchall()
    conn.close()

    categories = [row["category"] for row in rows]

    return render_template("manage_categories.html", categories=categories)

@app.route("/admin/categories/delete/<name>")
def delete_category(name):
    conn = get_db_connection()
    conn.execute("UPDATE posts SET category = NULL WHERE category = ?", (name,))
    conn.commit()
    conn.close()
    return redirect("/admin/categories")

@app.route("/admin/categories/confirm_delete/<name>")
def confirm_delete_category(name):
    return render_template("confirm_delete_category.html", category=name)




if __name__ == "__main__":
    app.run(debug=True)
