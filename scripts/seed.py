# seeds SQLite with demo data
"""
Seed the SQLite database with demo data.
Run once before starting the server:
    python scripts/seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.db.session import engine

DDL = """
CREATE TABLE IF NOT EXISTS books (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title   TEXT NOT NULL,
    author  TEXT NOT NULL,
    genre   TEXT NOT NULL,
    status  TEXT NOT NULL DEFAULT 'AVAILABLE',
    price   REAL NOT NULL DEFAULT 9.99
);

CREATE TABLE IF NOT EXISTS members (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email     TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS borrowings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id       INTEGER NOT NULL REFERENCES books(id),
    member_id     INTEGER NOT NULL REFERENCES members(id),
    borrow_date   TEXT NOT NULL,
    due_date      TEXT NOT NULL,
    returned_date TEXT,
    status        TEXT NOT NULL DEFAULT 'BORROWED'
);
"""

BOOKS = [
    ("The Great Gatsby",       "F. Scott Fitzgerald", "Classic",  "AVAILABLE", 12.99),
    ("To Kill a Mockingbird",  "Harper Lee",          "Classic",  "BORROWED",  11.99),
    ("1984",                   "George Orwell",       "Dystopian","OVERDUE",   10.99),
    ("Brave New World",        "Aldous Huxley",       "Dystopian","AVAILABLE",  9.99),
    ("The Hobbit",             "J.R.R. Tolkien",      "Fantasy",  "BORROWED",  14.99),
    ("Harry Potter I",         "J.K. Rowling",        "Fantasy",  "AVAILABLE", 13.99),
    ("Dune",                   "Frank Herbert",       "Sci-Fi",   "OVERDUE",   15.99),
    ("Foundation",             "Isaac Asimov",        "Sci-Fi",   "AVAILABLE", 11.99),
    ("Sapiens",                "Yuval Noah Harari",   "Non-Fiction","BORROWED", 16.99),
    ("Atomic Habits",          "James Clear",         "Non-Fiction","AVAILABLE",17.99),
    ("Clean Code",             "Robert C. Martin",    "Tech",     "BORROWED",  39.99),
    ("The Pragmatic Programmer","David Thomas",       "Tech",     "AVAILABLE", 44.99),
    ("Thinking Fast and Slow", "Daniel Kahneman",     "Psychology","OVERDUE",  13.99),
    ("Influence",              "Robert Cialdini",     "Psychology","AVAILABLE", 12.99),
    ("Rich Dad Poor Dad",      "Robert Kiyosaki",     "Finance",  "BORROWED",  10.99),
]

MEMBERS = [
    ("Alice Wanjiru",   "alice@demo.com"),
    ("Brian Otieno",    "brian@demo.com"),
    ("Carol Muthoni",   "carol@demo.com"),
    ("David Kimani",    "david@demo.com"),
    ("Eve Njeri",       "eve@demo.com"),
    ("Frank Ochieng",   "frank@demo.com"),
    ("Grace Akinyi",    "grace@demo.com"),
    ("Henry Mwangi",    "henry@demo.com"),
]

BORROWINGS = [
    # (book_id, member_id, borrow_date, due_date, returned_date, status)
    (1,  1, "2026-06-01", "2026-06-15", "2026-06-14", "RETURNED"),
    (2,  1, "2026-06-20", "2026-07-04", None,         "BORROWED"),
    (3,  1, "2026-05-01", "2026-05-15", None,         "OVERDUE"),
    (5,  2, "2026-06-10", "2026-06-24", "2026-06-23", "RETURNED"),
    (6,  2, "2026-07-01", "2026-07-15", None,         "BORROWED"),
    (7,  2, "2026-04-01", "2026-04-15", None,         "OVERDUE"),
    (9,  2, "2026-07-10", "2026-07-24", None,         "BORROWED"),
    (1,  3, "2026-05-15", "2026-05-29", "2026-05-28", "RETURNED"),
    (4,  3, "2026-06-05", "2026-06-19", "2026-06-18", "RETURNED"),
    (10, 3, "2026-07-05", "2026-07-19", None,         "BORROWED"),
    (11, 4, "2026-06-01", "2026-06-15", "2026-06-15", "RETURNED"),
    (12, 4, "2026-06-20", "2026-07-04", None,         "BORROWED"),
    (13, 4, "2026-04-10", "2026-04-24", None,         "OVERDUE"),
    (14, 4, "2026-07-01", "2026-07-15", None,         "BORROWED"),
    (15, 5, "2026-06-15", "2026-06-29", "2026-06-28", "RETURNED"),
    (8,  5, "2026-07-01", "2026-07-15", None,         "BORROWED"),
    (3,  6, "2026-05-20", "2026-06-03", None,         "OVERDUE"),
    (7,  6, "2026-06-10", "2026-06-24", "2026-06-23", "RETURNED"),
    (1,  7, "2026-07-01", "2026-07-15", None,         "BORROWED"),
    (5,  8, "2026-06-01", "2026-06-15", "2026-06-14", "RETURNED"),
    (9,  8, "2026-06-20", "2026-07-04", None,         "BORROWED"),
    (11, 1, "2026-07-10", "2026-07-24", None,         "BORROWED"),
    (13, 2, "2026-07-05", "2026-07-19", None,         "BORROWED"),
    (15, 3, "2026-07-08", "2026-07-22", None,         "BORROWED"),
]


def seed():
    with engine.connect() as conn:
        for stmt in DDL.strip().split(";"):
            stmt = stmt.strip()
            if stmt:
                conn.execute(text(stmt))

        # Idempotent — skip if already seeded
        existing = conn.execute(text("SELECT COUNT(*) FROM books")).scalar()
        if existing > 0:
            print("Database already seeded. Skipping.")
            return

        conn.execute(
            text("INSERT INTO books (title, author, genre, status, price) VALUES (:t,:a,:g,:s,:p)"),
            [{"t": b[0], "a": b[1], "g": b[2], "s": b[3], "p": b[4]} for b in BOOKS],
        )
        conn.execute(
            text("INSERT INTO members (full_name, email) VALUES (:n,:e)"),
            [{"n": m[0], "e": m[1]} for m in MEMBERS],
        )
        conn.execute(
            text("INSERT INTO borrowings (book_id,member_id,borrow_date,due_date,returned_date,status) VALUES (:bi,:mi,:bd,:dd,:rd,:s)"),
            [{"bi": b[0], "mi": b[1], "bd": b[2], "dd": b[3], "rd": b[4], "s": b[5]} for b in BORROWINGS],
        )
        conn.commit()
        print(f"Seeded {len(BOOKS)} books, {len(MEMBERS)} members, {len(BORROWINGS)} borrowings.")


if __name__ == "__main__":
    seed()