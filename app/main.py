from . import db, utils
from .users.models import User
from .shortcuts import render, redirect
from .videos.models import Video
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from .users.backends import JWTCookieBackend
from .users.decorators import login_required
from cassandra.cqlengine.management import sync_table
from .users.schemas import UserSignupSchema, UserLoginSchema
from app.videos.routers import router as video_router


DB_SESSION = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    sync_table(Video)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
app.include_router(video_router)

from .handlers import *

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {}, status_code=200)
    return render(request, "home.html", {})

@app.get("/account", response_class=HTMLResponse)
@login_required
def account_view_page(request: Request):
    context = {}
    return render(request, "account.html", context)

@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    session_id = request.cookies.get("cookies") or None
    return render(request, "auth/login.html", {"logged_in": session_id is not None})

@app.post("/login", response_class=HTMLResponse)
def login_post_view(
    request: Request, 
    email: str = Form(...),
    password: str = Form(...)):
    raw_data = {
    "email": email,
    "password": password,
    }
    
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    context = {
        "data": data,
        "errors": errors,
    }

    if data:
        cookies = {"cookies": data["session_id"]}
    
    if len(errors) > 0:
        return render(request, "auth/login.html", context, status_code=400)
    return redirect("/", cookies)

@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render(request, "auth/signup.html", {})

@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(
    request: Request, 
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...)):
    raw_data = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm,
    }

    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    context = {
        "data": data,
        "errors": errors,
    }
    
    if len(errors) > 0:
        return render(request, "auth/login.html", context, status_code=400)
    
    return redirect("/login")

@app.get("/users")
def users_list_view():
    q = User.objects().all().limit(10)
    return list(q)

@app.post("/watch-event")
def watch_event_view(request: Request, data: dict):
    print(data)
    print(request.user.is_authenticated)
    return {"working": True}