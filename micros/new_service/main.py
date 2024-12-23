from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="New Service")

Instrumentator().instrument(app).expose(app)