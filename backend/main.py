import os
from flask import Flask, render_template, request, redirect, url_for
import data

BASE_DIR = os.path.dirname (os.path.abspath(__file__))
ROOT_DIR = os.path.dirname (BASE_DIR)
FRONTEND_DIR = os.path.join (ROOT_DIR, "frontend")

app = Flask (__name__, template_folder=FRONTEND_DIR, static_folder=FRONTEND_DIR, static_url_path="/static")

@app.route('/', methods = ["GET", "POST"])
def index ():
    if request.method == "POST":
        title = request.form.get ("title")
        author = request.form.get ("author")
        isbn = request.form.get ("isbn")
        inv_number = request.form.get ("inv_number")
        shelf_nameber = request.form.get ("shelf_nameber")

        if title and author:
            data.add_book(title, author, isbn, inv_number, shelf_nameber)
        return redirect (url_for("index"))

    books = data.get_all_books()
    return render_template ("index.html", books=books)


if __name__ == '__main__':
    data.init_db()
    app.run(debug=True)
