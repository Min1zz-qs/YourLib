import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'library.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
                CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT,
                inv_number TEXT,
                shelf_nameber TEXT,
                status TEXT DEFAULT 'На полке'
            )
        """)

def add_book (title, author, isbn, inv_number, shelf_nameber):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO books (title, author, isbn, inv_number, shelf_nameber) VALUES (?, ?, ?, ?, ?)",
            (title, author, isbn, inv_number, shelf_nameber)
        )
        conn.commit()

def get_all_books():
    with get_connection() as conn:
        return conn.execute ("SELECT * FROM books ORDER BY id DESC").fetchall()
    
