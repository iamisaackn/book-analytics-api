# reusable CSV streaming utility
"""
Usage in any service:
    from app.utils.csv_exporter import dataframe_to_csv_response
    return dataframe_to_csv_response(df, "Report_Name", column_map={...})

Adding CSV export to a new endpoint = 3 steps:
    1. repo → add fetch_all_X() (no LIMIT/OFFSET)
    2. service → add export_X_csv() (call fetch_all, pass column_map)
    3. endpoint → add GET /X/export route (same filters, no pagination)
"""
import io
from datetime import datetime

from fastapi.responses import StreamingResponse


def generate_filename(report_name: str, extension: str = "csv") -> str:
    """e.g. Book_Report_2026-08-15_08-00.csv"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    safe_name = report_name.replace(" ", "_")
    return f"{safe_name}_{timestamp}.{extension}"


def dataframe_to_csv_response(
    df,
    report_name: str,
    column_map: dict[str, str] | None = None,
) -> StreamingResponse:
    """
    Converts a pandas DataFrame to a streaming CSV download response.

    Args:
        df: Full dataset DataFrame (no pagination).
        report_name:  Used in the downloaded filename.
        column_map: Optional — maps DataFrame column names to human-readable CSV headers.
                      e.g. {"book_id": "Book ID", "full_name": "Full Name"}
    """
    if column_map:
        df = df.rename(columns=column_map)

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={generate_filename(report_name)}",
            "Cache-Control": "no-cache",
        },
    )