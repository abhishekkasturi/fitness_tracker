from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

import os
import database
import auth
import dev_auth

app = FastAPI()
database.init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET")
)

# Landing page

@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse(
        "landing.html",
        {"request": request}
    )
# Home page after successfull login

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):

    if "user_id" not in request.session:
        return RedirectResponse("/login")

    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )
# Login Details

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.post("/login")
def login_user(
    request: Request,
    gym_code: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    conn = database.get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password_hash FROM users WHERE gym_code=%s AND username=%s",
        (gym_code, username)
    )
    user = cur.fetchone()
    conn.close()

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    user_id, password_hash = user

    if not auth.verify_password(password, password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    # Successful login → store user_id in session
    request.session["user_id"] = user_id

    return RedirectResponse("/home", status_code=303)

# Registration page

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )

@app.post("/register")
def register_user(
    gym_code: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    age: int = Form(...),
    sex: str = Form(...),
    height: float = Form(...)
):

    conn = database.get_connection()
    cur = conn.cursor()

    password_hash = auth.hash_password(password)

    cur.execute(
        """
        INSERT INTO users (gym_code, username, password_hash, age, sex, height)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (gym_code, username, password_hash, age, sex, height)
    )

    conn.commit()
    conn.close()

    return RedirectResponse("/login", status_code=303)

