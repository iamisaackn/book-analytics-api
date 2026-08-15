# GET /sales-summary, /export
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_for_user
from app.schemas.sales_summary import SalesSummaryPage
from app.services import sales_summary_service

router = APIRouter(prefix="/sales-summary", tags=["Sales Summary"])


@router.get("", response_model=SalesSummaryPage, summary="Sales Revenue by Genre")
def list_sales_summary(
    genre: str | None = Query(None, description="Filter by genre name"),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_for_user),
):
    return sales_summary_service.get_sales_summary(db, genre, offset, limit)


@router.get(
    "/export",
    summary="Export Sales Summary as CSV",
    response_class=StreamingResponse,
    responses={200: {"content": {"text/csv": {}}, "description": "CSV file download"}},
)
def export_sales_summary(
    genre: str | None = Query(None),
    db: Session = Depends(get_db_for_user),
):
    return sales_summary_service.export_sales_summary_csv(db, genre)