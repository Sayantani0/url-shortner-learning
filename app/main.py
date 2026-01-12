from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="URL Shortener (FastAPI + MySQL)")

app.include_router(router)