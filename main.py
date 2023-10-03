from fastapi import FastAPI, Request
from app.api.endpoints import upload, download
import time

app = FastAPI()



app.include_router(upload.router, prefix="/api")
app.include_router(download.router, prefix="/api")
