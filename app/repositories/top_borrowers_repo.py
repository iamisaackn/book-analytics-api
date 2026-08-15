import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

_BASE_SQL = """
    SELECT
        m.id AS member_id,
        m.full_name AS full_name,
        m.email AS email,
        COUNT(br.id) AS total_borrowed,
        COUNT(CASE WHEN br.returned_date IS NOT NULL THEN 1 END) AS total_returned,
        COUNT(CASE WHEN br.status = 'OVERDUE' THEN 1 END) AS total_overdue,
        (
            SELECT b2.genre
            FROM borrowings br2
            INNER JOIN books b2 ON b2.id = br2.book_id
            WHERE br2.member_id = m.id
            GROUP BY b2.genre
            ORDER BY COUNT(*) DESC
            LIMIT 1
        ) AS favourite_genre,
        MAX(DATE(br.borrow_date)) AS last_borrow_date
    FROM members m
    INNER JOIN borrowings br ON br.member_id = m.id
    WHERE (
        :search_term IS NULL
        OR LOWER(m.full_name) LIKE '%' || LOWER(:search_term) || '%'
        OR LOWER(m.email) LIKE '%' || LOWER(:search_term) || '%'
    )
    GROUP BY m.id, m.full_name, m.email
    HAVING COUNT(br.id) >= :min_borrows
"""

_ORDER_BY = " ORDER BY total_borrowed DESC, m.full_name ASC"


def fetch_top_borrowers(
    db: Session,
    search_term: str | None = None,
    min_borrows: int = 2,
    offset: int = 0,
    limit: int = 10,
) -> pd.DataFrame:
    query = text(f"{_BASE_SQL} {_ORDER_BY} LIMIT :limit OFFSET :offset")
    params = {
        "search_term": search_term,
        "min_borrows": min_borrows,
        "limit": limit,
        "offset": offset,
    }
    return pd.DataFrame(db.execute(query, params).mappings().all())


def count_top_borrowers(
    db: Session,
    search_term: str | None = None,
    min_borrows: int = 2,
) -> int:
    query = text(f"SELECT COUNT(*) AS total FROM ({_BASE_SQL}) AS counted")
    params = {"search_term": search_term, "min_borrows": min_borrows}
    row = db.execute(query, params).mappings().first()
    return row["total"] if row else 0


def fetch_all_top_borrowers(
    db: Session,
    search_term: str | None = None,
    min_borrows: int = 2,
) -> pd.DataFrame:
    """Fetches all records for CSV export — no pagination."""
    query = text(f"{_BASE_SQL} {_ORDER_BY}")
    params = {"search_term": search_term, "min_borrows": min_borrows}
    return pd.DataFrame(db.execute(query, params).mappings().all())