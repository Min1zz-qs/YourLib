import sqlite3
import os
from contextlib import contextmanager


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "library.db")


@contextmanager
def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT,
                inv_number TEXT NOT NULL UNIQUE,
                shelf_number TEXT NOT NULL,
                reading_status TEXT NOT NULL DEFAULT 'Не прочитана',
                copy_status TEXT NOT NULL DEFAULT 'На полке'
            )
        """)


def add_book(title, author, isbn, inv_number, shelf_number):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO books
            (title, author, isbn, inv_number, shelf_number)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, isbn, inv_number, shelf_number))


def get_all_books(
    search="",
    reading_status="",
    copy_status="",
    shelf_number="",
    sort_by="id",
    sort_order="desc"
):

    allowed_sort_fields = {
        "id": "id",
        "title": "title",
        "author": "author",
        "inv_number": "inv_number"
    }

    sort_column = allowed_sort_fields.get(sort_by, "id")
    sort_direction = "ASC" if sort_order == "asc" else "DESC"

    query = "SELECT * FROM books Where 1=1 "
    params = []

    if search:
        query += """
            AND (
                 title LIKE ?
                OR author LIKE ?
                OR isbn LIKE ?
                OR inv_number LIKE ?
            )
        """
        value = f"%{search}%"
        params.extend([value, value, value, value])

    if reading_status:
        query += "AND reading_status = ?"
        params.append(reading_status)

    if copy_status:
        query += "AND copy_status = ?"
        params.append(copy_status)

    if shelf_number:
        query += "AND shelf_number = ?"
        params.append(shelf_number)

    query += f" ORDER BY {sort_column} {sort_direction}"

    with get_connection() as conn:
        return conn.execute(query, params).fetchall()

def get_all_shelves():
    with get_connection() as conn:
        rows = conn.execute ("""
            SELECT DISTINCT shelf_number
            FROM books
            WHERE shelf_number IS NOT NULL
            AND shelf_number != ''
            ORDER BY shelf_number
        """).fetchall()

        return [row["shelf_number"] for row in rows]



def get_book_by_id(book_id):
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM books
            WHERE id = ?
        """, (book_id,)).fetchone()


def update_book(
    book_id,
    title,
    author,
    isbn,
    inv_number,
    shelf_number,
    reading_status,
    copy_status
):
    with get_connection() as conn:
        cursor = conn.execute("""
            UPDATE books
            SET title = ?,
                author = ?,
                isbn = ?,
                inv_number = ?,
                shelf_number = ?,
                reading_status = ?,
                copy_status = ?
            WHERE id = ?
        """, (
            title,
            author,
            isbn,
            inv_number,
            shelf_number,
            reading_status,
            copy_status,
            book_id
        ))

        return cursor.rowcount


def delete_book(book_id):
    with get_connection() as conn:
        cursor = conn.execute("""
            DELETE FROM books
            WHERE id = ?
        """, (book_id,))

        return cursor.rowcount
