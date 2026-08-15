from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.repositories import books_repo
from app.schemas.books import BookPage, BookRow, BookStatus
from app.utils.csv_exporter import dataframe_to_csv_response

_CSV_COLUMN_MAP = {
    "book_id": "Book ID",
    "title": "Title",
    "author": "Author",
    "genre": "Genre",
    "status": "Status",
    "times_borrowed":"Times Borrowed",
    "days_overdue": "Days Overdue",
}


def get_books(
    db: Session,
    search_term: str | None,
    status: BookStatus | None,
    offset: int,
    limit: int,
) -> BookPage:
    status_value = status.value if status else None
    df = books_repo.fetch_books(db, search_term, status_value, offset, limit)
    total = books_repo.count_books(db, search_term, status_value)
    rows = [BookRow(**r) for r in df.to_dict(orient="records")] if not df.empty else []
    return BookPage(data=rows, total_records=total, offset=offset, limit=limit)


def export_books_csv(
    db: Session,
    search_term: str | None,
    status: BookStatus | None,
) -> StreamingResponse:
    status_value = status.value if status else None
    df = books_repo.fetch_all_books(db, search_term, status_value)
    return dataframe_to_csv_response(df, "Book_Report", column_map=_CSV_COLUMN_MAP)