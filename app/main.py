from fastapi import FastAPI
from . import config, db
from cassandra.cqlengine.management import sync_table
from contextlib import asynccontextmanager
from .users.models import User

DB_SESSION = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    yield

app = FastAPI(lifespan=lifespan)
settings = config.get_settings()


@app.get("/")
def homepage():
    return {"hello": "world", "keyspace": settings.keyspace}

@app.get("/users")
def users_list_view():
    q = User.objects().all().limit(10)
    return list(q)