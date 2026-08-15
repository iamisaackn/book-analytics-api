import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

_BASE_SQL = """
    SELECT
        b.id          AS book_id,
        b.title       AS title,
        b.author      AS author,
        b.genre       AS genre,
        b.status      AS status,
        COUNT(br.id)  AS times_borrowed,
        COALESCE(
            CAST(
                (julianday('now') - julianday(MAX(br.due_date))) AS INTEGER
            ), 0
        ) AS days_overdue
    FROM books b
    LEFT JOIN borrowings br ON br.book_id = b.id
    WHERE (
        :search_term IS NULL
        OR LOWER(b.title)  LIKE '%' || LOWER(:search_term) || '%'
        OR LOWER(b.author) LIKE '%' || LOWER(:search_term) || '%'
        OR LOWER(b.genre)  LIKE '%' || LOWER(:search_term) || '%'
    )
    AND (:status IS NULL OR b.status = :status)
    GROUP BY b.id, b.title, b.author, b.genre, b.status
"""

_ORDER_BY = " ORDER BY times_borrowed DESC, b.title ASC"


def fetch_books(
    db: Session,
    search_term: str | None = None,
    status: str | None = None,
    offset: int = 0,
    limit: int = 10,
) -> pd.DataFrame:
    query = text(f"{_BASE_SQL} {_ORDER_BY} LIMIT :limit OFFSET :offset")
    params = {"search_term": search_term, "status": status, "limit": limit, "offset": offset}
    return pd.DataFrame(db.execute(query, params).mappings().all())


def count_books(
    db: Session,
    search_term: str | None = None,
    status: str | None = None,
) -> int:
    query = text(f"SELECT COUNT(*) AS total FROM ({_BASE_SQL}) AS counted")
    params = {"search_term": search_term, "status": status}
    row = db.execute(query, params).mappings().first()
    return row["total"] if row else 0


def fetch_all_books(
    db: Session,
    search_term: str | None = None,
    status: str | None = None,
) -> pd.DataFrame:
    """Fetches all records for CSV export — no pagination."""
    query = text(f"{_BASE_SQL} {_ORDER_BY}")
    params = {"search_term": search_term, "status": status}
    return pd.DataFrame(db.execute(query, params).mappings().all())