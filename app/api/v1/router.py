# aggregates all routers
from fastapi import APIRouter

from app.api.v1.endpoints import books, health, sales_summary, top_borrowers

api_router = APIRouter()

api_router.include_router(health.router)

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(books.router)
v1_router.include_router(sales_summary.router)
v1_router.include_router(top_borrowers.router)

api_router.include_router(v1_router)