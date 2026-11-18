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
                inv_number TEXT,
                shelf_number TEXT,
                status TEXT DEFAULT 'На полке'
            )
        """)


def add_book(title, author, isbn, inv_number, shelf_number):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO books (title, author, isbn, inv_number, shelf_number)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, author, isbn, inv_number, shelf_number),
        )


def get_all_books():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM books ORDER BY id DESC"
        ).fetchall()


def get_book_by_id(book_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()


def update_book(book_id, title, author, isbn, inv_number, shelf_number):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE books
            SET title = ?, author = ?, isbn = ?, inv_number = ?, shelf_number = ?
            WHERE id = ?
            """,
            (title, author, isbn, inv_number, shelf_number, book_id),
        )
        return cursor.rowcount > 0


def delete_book(book_id):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,),
        )
        return cursor.rowcount > 0
