# get_db dependency
from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db


def get_db_for_user(
    _user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Generator[Session, None, None]:
    """
    Auth-gated DB dependency.
    Verifies the API key first, then yields the DB session.
    Mirrors the get_db_for_tenant pattern from multi-tenant production setup.
    """
    yield db