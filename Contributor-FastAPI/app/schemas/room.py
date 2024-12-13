from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class RoomBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Properties to receive on room creation
class RoomCreate(RoomBase):
    name: str

# Properties to receive on room update
class RoomUpdate(RoomBase):
    pass

# Properties shared by models stored in DB
class RoomInDBBase(RoomBase):
    id: int
    name: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return to client
class Room(RoomInDBBase):
    pass
