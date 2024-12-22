from fastapi import FastAPI
from routes import users_router, announcements_router, responses_router
from database import Base, engine
from prometheus_fastapi_instrumentator import Instrumentator


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Database Service")

app.include_router(users_router)
app.include_router(announcements_router)
app.include_router(responses_router)

Instrumentator().instrument(app).expose(app)
