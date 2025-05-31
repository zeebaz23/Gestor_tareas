from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from auth import create_user, authenticate_user
from database import create_connection


web_router = APIRouter()
templates = Jinja2Templates(directory="src/view/web")

session = {}

@web_router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@web_router.post("/login")
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        return RedirectResponse("/tasks", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "message": "Usuario o contraseña incorrectos"})

@web_router.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "message": ""})

@web_router.post("/register")
def register_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if create_user(username, password):
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse("register.html", {"request": request, "message": "El nombre de usuario ya existe"})

@web_router.get("/logout")
def logout():
    session.clear()
    return RedirectResponse("/login", status_code=302)

@web_router.get("/tasks", response_class=HTMLResponse)
def tasks_get(request: Request):
    if 'user_id' not in session:
        return RedirectResponse("/login", status_code=302)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, text, created_at, category, status FROM tasks WHERE user_id = ?', (session['user_id'],))
    tasks = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks, "username": session['username']})

@web_router.post("/tasks")
def tasks_post(request: Request, text: str = Form(...), category: str = Form(...), status: str = Form(...)):
    if 'user_id' not in session:
        return RedirectResponse("/login", status_code=302)
    if len(text) > 200:
        return RedirectResponse("/tasks", status_code=302)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (user_id, text, category, status) VALUES (?, ?, ?, ?)',
                   (session['user_id'], text, category, status))
    conn.commit()
    conn.close()
    return RedirectResponse("/tasks", status_code=302)

@web_router.get("/delete/{task_id}")
def delete_task(task_id: int):
    if 'user_id' not in session:
        return RedirectResponse("/login", status_code=302)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, session['user_id']))
    conn.commit()
    conn.close()
    return RedirectResponse("/tasks", status_code=302)

@web_router.get("/edit/{task_id}", response_class=HTMLResponse)
def edit_task_get(request: Request, task_id: int):
    if 'user_id' not in session:
        return RedirectResponse("/login", status_code=302)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT text, category, status FROM tasks WHERE id = ? AND user_id = ?', (task_id, session['user_id']))
    task = cursor.fetchone()
    conn.close()
    if not task:
        return RedirectResponse("/tasks", status_code=302)
    return templates.TemplateResponse("edit_task.html", {"request": request, "task": task, "id": task_id})

@web_router.post("/edit/{task_id}")
def edit_task_post(request: Request, task_id: int, text: str = Form(...), category: str = Form(...), status: str = Form(...)):
    if 'user_id' not in session:
        return RedirectResponse("/login", status_code=302)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET text = ?, category = ?, status = ? WHERE id = ? AND user_id = ?',
                   (text, category, status, task_id, session['user_id']))
    conn.commit()
    conn.close()
    return RedirectResponse("/tasks", status_code=302)
