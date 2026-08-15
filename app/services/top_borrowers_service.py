from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.repositories import top_borrowers_repo
from app.schemas.top_borrowers import TopBorrowerPage, TopBorrowerRow
from app.utils.csv_exporter import dataframe_to_csv_response

_CSV_COLUMN_MAP = {
    "member_id": "Member ID",
    "full_name": "Full Name",
    "email": "Email",
    "total_borrowed": "Total Borrowed",
    "total_returned": "Total Returned",
    "total_overdue": "Total Overdue",
    "favourite_genre": "Favourite Genre",
    "last_borrow_date":"Last Borrow Date",
}


def get_top_borrowers(
    db: Session,
    search_term: str | None,
    min_borrows: int,
    offset: int,
    limit: int,
) -> TopBorrowerPage:
    df = top_borrowers_repo.fetch_top_borrowers(db, search_term, min_borrows, offset, limit)
    total = top_borrowers_repo.count_top_borrowers(db, search_term, min_borrows)
    rows = [TopBorrowerRow(**r) for r in df.to_dict(orient="records")] if not df.empty else []
    return TopBorrowerPage(data=rows, total_records=total, offset=offset, limit=limit)


def export_top_borrowers_csv(
    db: Session,
    search_term: str | None,
    min_borrows: int,
) -> StreamingResponse:
    df = top_borrowers_repo.fetch_all_top_borrowers(db, search_term, min_borrows)
    return dataframe_to_csv_response(df, "Top_Borrowers", column_map=_CSV_COLUMN_MAP)