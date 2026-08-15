# GET /books, GET /books/export
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_for_user
from app.schemas.books import BookPage, BookStatus
from app.services import books_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=BookPage, summary="Book Catalogue Report")
def list_books(
    search_term: str | None = Query(None, description="Search by title, author or genre"),
    status: BookStatus | None = Query(None, description="Filter by status: AVAILABLE, BORROWED, OVERDUE"),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_for_user),
):
    return books_service.get_books(db, search_term, status, offset, limit)


@router.get(
    "/export",
    summary="Export Book Catalogue as CSV",
    response_class=StreamingResponse,
    responses={200: {"content": {"text/csv": {}}, "description": "CSV file download"}},
)
def export_books(
    search_term: str | None = Query(None),
    status: BookStatus | None = Query(None),
    db: Session = Depends(get_db_for_user),
):
    return books_service.export_books_csv(db, search_term, status)