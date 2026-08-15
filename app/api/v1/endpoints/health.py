# GET /actuator/health
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/actuator/health")
def healthcheck():
    return {"status": "up"}