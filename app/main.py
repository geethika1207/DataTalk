from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import models
from .db.database import engine, Base
from .routers import auth, datasets, query

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lovable.dev", "https://*.lovable.app", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(datasets.router)
app.include_router(query.router)