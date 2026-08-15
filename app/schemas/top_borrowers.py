# TopBorrowerRow, TopBorrowerPage
from pydantic import BaseModel
from app.schemas.common import PaginatedResponse


class TopBorrowerRow(BaseModel):
    member_id: int
    full_name: str
    email: str
    total_borrowed: int
    total_returned: int
    total_overdue: int
    favourite_genre: str | None = None
    last_borrow_date: str | None = None


class TopBorrowerPage(PaginatedResponse):
    data: list[TopBorrowerRow]