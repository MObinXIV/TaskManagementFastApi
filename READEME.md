# Task Management API

A lightweight **Task Management System** built with [**FastAPI**](https://fastapi.tiangolo.com/), [**SQLModel**](https://sqlmodel.tiangolo.com/), and **SQLite**, supporting advanced filtering, search, and sorting.

---

## Features

- Full CRUD: Create, Read, Update, Delete tasks  
- Search by title or description  
- Filter by status or priority  
- Sort by creation date or due date  
- SQLite as the default database  
- Configurable using `.env` file  
- Interactive API docs (Swagger & ReDoc)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/MObinXIV/TaskManagementFastApi.git
cd TaskManagementFastApi

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt
