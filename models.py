from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime

#Enum for the task status
class TaskStatus(str,Enum):
    PENDING = "pending"
    IN_PROGRESS ="in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Task(SQLModel,table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    title: str= Field(max_length=200)
    description: Optional[str]= Field(default=None,max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority=Field(default=TaskPriority.MEDIUM)
    created_at: datetime= Field(default_factory=datetime.now)
    updated_at: Optional[datetime]=None
    due_date: Optional[datetime]= None #Deadline of the task
    assigned_to: Optional[str]= Field(default=None, max_length=100)  
    
