from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import User, UserUpdate
from app.core.auth import get_current_user
from app.services import user_service
from app.db.session import get_db

router = APIRouter()

@router.get("/me", response_model=User)
def get_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update own user.
    """
    user = user_service.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.get("/{username}", response_model=User)
def get_user_by_username(
    username: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get user by username.
    """
    user = user_service.get_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user
