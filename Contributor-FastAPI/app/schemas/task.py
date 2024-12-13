from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.task import TaskStatus

# Shared properties
class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    room_id: Optional[int] = None
    status: Optional[TaskStatus] = None

# Properties to receive on task creation
class TaskCreate(TaskBase):
    title: str
    room_id: int

# Properties to receive on task update
class TaskUpdate(TaskBase):
    pass

# Properties shared by models stored in DB
class TaskInDBBase(TaskBase):
    id: int
    title: str
    assignee_id: Optional[int] = None
    github_branch: Optional[str] = None
    github_pr_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Properties to return to client
class Task(TaskInDBBase):
    pass
