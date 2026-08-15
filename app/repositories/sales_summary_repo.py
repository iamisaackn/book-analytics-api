import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

_BASE_SQL = """
    SELECT
        b.genre AS genre,
        COUNT(br.id) AS total_sales,
        ROUND(SUM(b.price), 2) AS total_revenue,
        ROUND(AVG(b.price), 2) AS avg_price,
        CASE
            WHEN PERCENT_RANK() OVER (ORDER BY SUM(b.price)) >= 0.66 THEN 'HIGH'
            WHEN PERCENT_RANK() OVER (ORDER BY SUM(b.price)) >= 0.33 THEN 'MEDIUM'
            ELSE 'LOW'
        END AS segment
    FROM borrowings br
    INNER JOIN books b ON b.id = br.book_id
    WHERE (:genre IS NULL OR LOWER(b.genre) LIKE '%' || LOWER(:genre) || '%')
    GROUP BY b.genre
    HAVING COUNT(br.id) > 0
"""

_ORDER_BY = " ORDER BY total_revenue DESC"


def fetch_sales_summary(
    db: Session,
    genre: str | None = None,
    offset: int = 0,
    limit: int = 10,
) -> pd.DataFrame:
    query = text(f"{_BASE_SQL} {_ORDER_BY} LIMIT :limit OFFSET :offset")
    params = {"genre": genre, "limit": limit, "offset": offset}
    return pd.DataFrame(db.execute(query, params).mappings().all())


def count_sales_summary(
    db: Session,
    genre: str | None = None,
) -> int:
    query = text(f"SELECT COUNT(*) AS total FROM ({_BASE_SQL}) AS counted")
    params = {"genre": genre}
    row = db.execute(query, params).mappings().first()
    return row["total"] if row else 0


def fetch_all_sales_summary(
    db: Session,
    genre: str | None = None,
) -> pd.DataFrame:
    """Fetches all records for CSV export — no pagination."""
    query = text(f"{_BASE_SQL} {_ORDER_BY}")
    params = {"genre": genre}
    return pd.DataFrame(db.execute(query, params).mappings().all())