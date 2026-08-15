# GET /top-borrowers, /export
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_for_user
from app.schemas.top_borrowers import TopBorrowerPage
from app.services import top_borrowers_service

router = APIRouter(prefix="/top-borrowers", tags=["Top Borrowers"])


@router.get("", response_model=TopBorrowerPage, summary="Top Borrowers Report")
def list_top_borrowers(
    search_term: str | None = Query(None, description="Search by name or email"),
    min_borrows: int = Query(default=2, ge=1, description="Minimum number of borrows"),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_for_user),
):
    return top_borrowers_service.get_top_borrowers(db, search_term, min_borrows, offset, limit)


@router.get(
    "/export",
    summary="Export Top Borrowers as CSV",
    response_class=StreamingResponse,
    responses={200: {"content": {"text/csv": {}}, "description": "CSV file download"}},
)
def export_top_borrowers(
    search_term: str | None = Query(None),
    min_borrows: int = Query(default=2, ge=1),
    db: Session = Depends(get_db_for_user),
):
    return top_borrowers_service.export_top_borrowers_csv(db, search_term, min_borrows)