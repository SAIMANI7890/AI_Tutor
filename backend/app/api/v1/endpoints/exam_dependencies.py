"""
Exam API Dependencies - Phase 4C
Reusable FastAPI dependency functions specific to examination endpoints.
"""
from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.test_repository import TestRepository


def get_exam_or_404(
    test_id: UUID = Path(..., description="UUID of the examination"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Dependency that:
    1. Validates test_id is a valid UUID (FastAPI does this automatically).
    2. Fetches the Test from the database.
    3. Returns 404 if not found.
    4. Returns 403 if the current user is not the owner.

    Usage in a route::

        @router.get("/{test_id}")
        def my_endpoint(test=Depends(get_exam_or_404)):
            ...

    Returns:
        Tuple[Test, User] — the verified test and the current user.
    """
    test = TestRepository.get_by_id(db, test_id)
    if test is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found.",
        )
    if test.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this exam.",
        )
    return test, current_user
