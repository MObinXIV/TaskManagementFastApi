from fastapi import FastAPI,HTTPException, status,Depends , Query
from sqlmodel import Session, select
from models import Task, TaskStatus, TaskPriority
from database import get_session, init_db 
from contextlib import asynccontextmanager
from schemas import TaskCreate, TaskUpdate, TaskResponse
from datetime import datetime
from typing import List,Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  
    yield  
app = FastAPI(lifespan=lifespan)
@app.get("/",tags=["Root"])
async def readRoot():
    return {
        "message": "Task Management API",
        "endpoints": [
            "GET /health",
            "POST /tasks",
            "GET /tasks",
            "GET /tasks/{task_id}",
            "patch /tasks/{task_id}",
            "DELETE /tasks/{task_id}",
            "GET /tasks/status/{status}",
            "GET /tasks/priority/{priority}",
        ]
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}

@app.post("/tasks",response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
def createTask(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task(**task.model_dump()) #converts the input data (task) into a Task object for the database
    session.add(db_task)#Adds the new task to the session (ready to be saved)
    session.commit() #Saves the task into the database permanently
    session.refresh(db_task) #Reloads the task from the DB so it has the generated id and timestamps
    return db_task

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    search: Optional[str] = None,
    sort_by: str = Query("created_at", enum=["created_at", "due_date", "priority", "title"]),
    order: str = Query("asc", enum=["asc", "desc"]),
    session: Session = Depends(get_session),
):# Start with base query
    statement = select(Task)

    # Search filter (optional)
    if search:
        statement = statement.where(
            Task.title.contains(search) | Task.description.contains(search)
        )

    #  Sorting
    column = getattr(Task, sort_by)
    if order == "desc":
        column = column.desc()
    statement = statement.order_by(column)

    # Pagination
    statement = statement.offset(skip).limit(limit)

    return session.exec(statement).all()


@app.get("/tasks/{taskId}",response_model=TaskResponse)
def getTaskById(taskId:int,
                session: Session=Depends(get_session)
                ):
    task = session.get(Task,taskId)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def updateTask(
    task_id: int,
    taskUpdate: TaskUpdate,
    session: Session = Depends(get_session)
):
    dbTask = session.get(Task, task_id)
    if not dbTask:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updateData = taskUpdate.model_dump(exclude_unset=True)
    for key, value in updateData.items():
        setattr(dbTask, key, value)

    dbTask.updated_at = datetime.now()  

    session.commit()
    session.refresh(dbTask)
    return dbTask


@app.delete("/tasks/{taskId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(taskId: int, session: Session = Depends(get_session)):
    task = session.get(Task, taskId)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return None

@app.get("/tasks/status/{status}",response_model=List[TaskResponse])
def getByStatus(
        status:TaskStatus,
        session:Session=Depends(get_session)
):
    statement= select(Task).where(Task.status==status)
    tasks=session.exec(statement).all()
    return tasks

@app.get("/tasks/priority/{priority}", response_model=List[TaskResponse])
def getByPriority(priority: TaskPriority,
    session: Session = Depends(get_session)):
    statement = select(Task).where(Task.priority == priority)
    tasks = session.exec(statement).all()
    return tasks