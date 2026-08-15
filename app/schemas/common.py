# PaginationMeta
from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    """Base pagination schema — all paginated endpoints extend this."""
    total_records: int
    offset: int
    limit: int