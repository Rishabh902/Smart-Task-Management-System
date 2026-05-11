# Smart Task Management System

A Flask-based Smart Task Management System with:

- User Authentication
- Task CRUD APIs
- PostgreSQL Integration
- Pandas & NumPy Analytics
- WebSocket Real-Time Updates
- Responsive Frontend UI

---

# Features

## Authentication
- User Registration
- User Login
- Logout Functionality

## Task Management
- Add Task
- Update Task
- Delete Task
- Get All Tasks

## Analytics
- Total Tasks
- Completed Tasks
- Pending Tasks
- Completion Percentage

## Real-Time Features
- Live Task Updates using WebSockets

## Frontend
- Responsive Dashboard
- Task List UI
- Analytics Summary Cards

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Language |
| Flask | Web Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Flask-Login | Authentication |
| Flask-SocketIO | WebSockets |
| Pandas | Analytics |
| NumPy | Calculations |
| HTML/CSS | Frontend |
| Bootstrap | Responsive Design |

---


# Database Schema

## Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

## Tasks Table

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    priority VARCHAR(50),
    status VARCHAR(50),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id)
);
```

---

# Installation & Setup

## Step 1: Clone Repository

```bash
git clone https://github.com/your-username/smart-task-manager.git

cd smart-task-manager
```

---

## Step 2: Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Setup

## Step 1: Create Database

Open pgAdmin or PostgreSQL terminal.

```sql
CREATE DATABASE smart_task_db;
```

---

## Step 2: Configure Database

Open:

```plaintext
config.py
```

Update:

```python
SQLALCHEMY_DATABASE_URI = (
    "postgresql://postgres:your_password@localhost:5432/smart_task_db"
)
```

Replace:

```plaintext
your_password
```

with your PostgreSQL password.

---

# Run Application

```bash
python app.py
```

Server will run on:

```plaintext
http://127.0.0.1:5000
```

---

# WebSocket Feature

Implemented using Flask-SocketIO.

Features:
- Live task updates
- Real-time notifications

---

# Screenshots

## Login Page
- User login form

## Register Page
- User registration form

## Dashboard
- Task list
- Analytics cards
- Real-time updates

---

# Future Improvements

- JWT Authentication
- Task Search & Filter
- Dark Mode
- Email Notifications
- Charts & Graphs
- Task Deadlines

---
