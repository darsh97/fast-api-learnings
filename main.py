from fastapi import FastAPI, Request
from app.api.endpoints import upload, download
from app.api.middlewares.response_time_middle_ware import ProcessTimeMiddleware

import time

app = FastAPI()

app.add_middleware(ProcessTimeMiddleware)

app.include_router(upload.router, prefix="/api")
app.include_router(download.router, prefix="/api")
