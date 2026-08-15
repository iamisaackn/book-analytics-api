from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.repositories import sales_summary_repo
from app.schemas.sales_summary import SalesSummaryPage, SalesSummaryRow
from app.utils.csv_exporter import dataframe_to_csv_response

_CSV_COLUMN_MAP = {
    "genre":         "Genre",
    "total_sales":   "Total Sales",
    "total_revenue": "Total Revenue",
    "avg_price":     "Avg Price",
    "segment":       "Revenue Segment",
}


def get_sales_summary(
    db: Session,
    genre: str | None,
    offset: int,
    limit: int,
) -> SalesSummaryPage:
    df = sales_summary_repo.fetch_sales_summary(db, genre, offset, limit)
    total = sales_summary_repo.count_sales_summary(db, genre)
    rows = [SalesSummaryRow(**r) for r in df.to_dict(orient="records")] if not df.empty else []
    return SalesSummaryPage(data=rows, total_records=total, offset=offset, limit=limit)


def export_sales_summary_csv(
    db: Session,
    genre: str | None,
) -> StreamingResponse:
    df = sales_summary_repo.fetch_all_sales_summary(db, genre)
    return dataframe_to_csv_response(df, "Sales_Summary", column_map=_CSV_COLUMN_MAP)