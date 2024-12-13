from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.models.user import User
from app.core.auth import get_current_user
from app.services import task_service, github_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[Task])
def get_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve tasks.
    """
    return task_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Task)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new task.
    """
    task = task_service.create(db, obj_in=task_in, creator_id=current_user.id)
    return task

@router.get("/{task_id}", response_model=Task)
def get_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get task by ID.
    """
    task = task_service.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    task_in: TaskUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update task.
    """
    task = task_service.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.assignee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    task = task_service.update(db, db_obj=task, obj_in=task_in)
    return task

@router.post("/{task_id}/start")
def start_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Start working on a task.
    """
    task = task_service.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Create GitHub branch and update task
    branch_name = github_service.create_branch_for_task(task)
    task = task_service.start_task(db, task=task, user=current_user, branch_name=branch_name)
    return task

@router.post("/{task_id}/join")
def join_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Join a task as a contributor.
    """
    task = task_service.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = task_service.join_task(db, task=task, user=current_user)
    return task
