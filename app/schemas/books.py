# BookRow, BookPage, BookStatus enum
from enum import Enum
from pydantic import BaseModel
from app.schemas.common import PaginatedResponse


class BookStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    BORROWED = "BORROWED"
    OVERDUE = "OVERDUE"


class BookRow(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    status: BookStatus
    times_borrowed: int
    days_overdue: int


class BookPage(PaginatedResponse):
    data: list[BookRow]