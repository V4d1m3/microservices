import logging
from fastapi import FastAPI
from routes import router
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO, filename='auth_service.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = FastAPI(title="Auth Service")
app.include_router(router)

Instrumentator().instrument(app).expose(app)