from fastapi import FastAPI
from src.routes import endpoint1

app = FastAPI()

app.include_router(endpoint1.router)