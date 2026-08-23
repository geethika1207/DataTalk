from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routers import auth, datasets, query


# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
Path("uploads").mkdir(exist_ok=True)

# 2. Initialize App
app = FastAPI(title="DataTalk API")

# 3. Allow all connections (Simplest CORS setup)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# 4. Attach your routes
app.include_router(auth.router)
app.include_router(datasets.router)
app.include_router(query.router)