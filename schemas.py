from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from models import TaskStatus, TaskPriority

class TaskCreate(BaseModel):
    title:str
    description: Optional[str]="pending"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    
    @field_validator("title")
    @classmethod
    def checkValidTitle(cls,value):
        if not value.strip(): #check if the value is valid after removing the spaces
            raise ValueError("Title can't be empty, please enter the task title")
        return value.strip()
    @field_validator("due_date")
    @classmethod
    def checkValidDeadLine(cls,value):
        if value and value< datetime.now():
            raise ValueError("Deadline must be future value")
        return value

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None

    class Config:
        orm_mode = True 