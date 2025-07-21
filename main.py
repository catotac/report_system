from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import router as api_router

app = FastAPI()
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="frontend"), name="static")
