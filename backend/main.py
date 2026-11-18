import os
from flask import Flask, render_template, request, redirect, url_for
import data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

app = Flask (
    __name__, 
    template_folder=FRONTEND_DIR, 
    static_folder=FRONTEND_DIR, 
    static_url_path="/static"
    )

data.init_db()

@app.route('/', methods = ["GET", "POST"])
def index ():
    if request.method == "POST":
        title = request.form.get ("title", "").strip()
        author = request.form.get ("author", "").strip()
        isbn = request.form.get ("isbn", "").strip()
        inv_number = request.form.get ("inv_number", "").strip()
        shelf_number = request.form.get ("shelf_number", "").strip()

        if title and author and inv_number and shelf_number:
            data.add_book(
                title, 
                author, 
                isbn or None, 
                inv_number, 
                shelf_number
                )
        return redirect (url_for("index"))

    books = data.get_all_books()
    return render_template ("index.html", books=books)


if __name__ == '__main__':
    app.run(debug=True)
