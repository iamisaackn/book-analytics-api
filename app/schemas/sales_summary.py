# SalesSummaryRow, SalesSummaryPage
from enum import Enum
from pydantic import BaseModel
from app.schemas.common import PaginatedResponse


class RevenueSegment(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class SalesSummaryRow(BaseModel):
    genre: str
    total_sales: int
    total_revenue: float
    avg_price: float
    segment: RevenueSegment


class SalesSummaryPage(PaginatedResponse):
    data: list[SalesSummaryRow]