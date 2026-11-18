import os
from flask import Flask, abort, redirect, render_template, request, url_for
import data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=FRONTEND_DIR,
    static_url_path="/static",
)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        isbn = request.form.get("isbn", "").strip()
        inv_number = request.form.get("inv_number", "").strip()
        shelf_number = request.form.get("shelf_number", "").strip()

        # Проверяем данные и на сервере, а не только атрибутами HTML required.
        if all((title, author, isbn, inv_number, shelf_number)):
            data.add_book(title, author, isbn, inv_number, shelf_number)

        return redirect(url_for("index"))

    books = data.get_all_books()
    return render_template("index.html", books=books)


@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = data.get_book_by_id(book_id)
    if book is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        isbn = request.form.get("isbn", "").strip()
        inv_number = request.form.get("inv_number", "").strip()
        shelf_number = request.form.get("shelf_number", "").strip()

        if not all((title, author, isbn, inv_number, shelf_number)):
            return render_template(
                "edit_book.html",
                book=book,
                error="Заполните все поля.",
            ), 400

        data.update_book(
            book_id,
            title,
            author,
            isbn,
            inv_number,
            shelf_number,
        )
        return redirect(url_for("index"))

    return render_template("edit_book.html", book=book)


@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    if not data.delete_book(book_id):
        abort(404)

    return redirect(url_for("index"))


if __name__ == "__main__":
    data.init_db()
    app.run(debug=True)
