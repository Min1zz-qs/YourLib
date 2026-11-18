import os
from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for,
    abort
)
import data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

READING_STATUSES = [
    "Не прочитана",
    "Читаю",
    "Прочитана"
]

COPY_STATUSES = [
    "На полке",
    "Одолжена",
    "Утеряна",
    "Библиотечная"
]

app = Flask (
    __name__, 
    template_folder=FRONTEND_DIR, 
    static_folder=FRONTEND_DIR, 
    static_url_path="/static"
    )

data.init_db()

def get_book_from_data():
    return {
        "title": request.form.get("title"),
        "author": request.form.get ("author", "").strip(),
        "isbn": request.form.get ("isbn", "").strip() or None,
        "inv_number": request.form.get ("inv_number", "").strip(),
        "shelf_number": request.form.get ("shelf_number", "").strip(),
        "reading_status": request.form.get ("Reading_status", "Не прочитана").strip(),
        "copy_status": request.form.get ("copy_status", "На полке").strip()
    }
def validate_book (book):
    if not all ([
        book["title"],
        book["author"],
        book["inv_number"],
        book["Shelf_number"]
    ]):
        return "Заполните все обязательные поля."

    if book ["reading_status"] not in READING_STATUSES:
        return "Недопустимый статус чтения."

    if book["copy_status"] not in COPY_STATUSES:
        return "Недопустимый статус экземпляра."

    return None

@app.route('/', methods = ["GET", "POST"])
def index ():
    error = None

    if request.method == "POST":
        book = get_book_from_data()
        error = validate_book(book)

        if error is None:
            try:
                data.add_book(
                    book["title"],
                    book["author"],
                    book["isbn"],
                    book["inv_number"],
                    book["shelf_number"]
                )
                return redirect(url_for("index"))

            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    error = "Книга с таким инвентарным номером уже существует."
                else:
                    raise
            
    books = data.get_template(
        "index.html",
        books = books,
        error = error
    )

@app.route("/book/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
        book = data.get_book_by_id(book_id)

        if book is None:
            abort(404)

        error = None

        if request.method == "POST":
            form_data = get_book_from_data()
            error = validate_book(form_data)

            if error is None:
                try:
                    data.update_book(
                        form_data["title"],
                        form_data["author"],
                        form_data["isbn"],
                        form_data["inv_number"],
                        form_data["shelf_number"],
                        form_data["reading_status"],
                        form_data["copy_status"],
                    )

                    return redirect(url_for("index"))

                except Exception as e:
                    if "UNIQUE constraint failed" in str(e):
                        error = "Книга с таким инвентарным номером уже существует."
                    else:
                        raise
            book = {
                **form_data,
                "id": book_id
            }

        return render_template(
            "edit_book.html",
            book = book,
            error = error,
            reading_statuses = READING_STATUSES,
            copy_statuses = COPY_STATUSES            
        )
 
        

@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
        deleted = data.delete_book(book_id)

        if deleted == 0:
            abort(404)

        return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
