from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.room import Room, RoomCreate, RoomUpdate
from app.models.user import User
from app.core.auth import get_current_user
from app.services import room_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[Room])
def get_rooms(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve rooms.
    """
    return room_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Room)
def create_room(
    *,
    db: Session = Depends(get_db),
    room_in: RoomCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new room.
    """
    room = room_service.create(db, obj_in=room_in, owner_id=current_user.id)
    return room

@router.get("/{room_id}", response_model=Room)
def get_room(
    *,
    db: Session = Depends(get_db),
    room_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get room by ID.
    """
    room = room_service.get(db, id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.put("/{room_id}", response_model=Room)
def update_room(
    *,
    db: Session = Depends(get_db),
    room_id: int,
    room_in: RoomUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update room.
    """
    room = room_service.get(db, id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    room = room_service.update(db, db_obj=room, obj_in=room_in)
    return room

@router.delete("/{room_id}")
def delete_room(
    *,
    db: Session = Depends(get_db),
    room_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete room.
    """
    room = room_service.get(db, id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    room = room_service.remove(db, id=room_id)
    return {"success": True}
