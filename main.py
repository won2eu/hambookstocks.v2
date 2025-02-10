from fastapi import FastAPI
from app.dependencies.db import *
from app.routers import auth_routers

create_db_and_table()

app = FastAPI()
app.include_router(auth_routers.router)
