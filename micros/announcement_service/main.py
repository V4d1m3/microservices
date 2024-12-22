import logging
from fastapi import FastAPI
from routes import announcements_router, responses_router
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware
import os

# Настройки конфигурации
LOG_FILE = os.getenv("LOG_FILE", "announcement_service.log")

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация FastAPI приложения
app = FastAPI(
    title="Announcement Service",
    description="Сервис для публикации и взаимодействия с объявлениями",
    version="1.0.0"
)

# Подключение маршрутизаторов
app.include_router(announcements_router)
app.include_router(responses_router)

# Middleware для CORS (если требуется)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Лучше заменить на список доверенных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инструментатор Prometheus
Instrumentator().instrument(app).expose(app)

# Логируем сообщение о старте сервиса
@app.on_event("startup")
async def startup_event():
    logger.info("Announcement Service запущен и готов к работе.")

# Логируем событие остановки сервиса
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Announcement Service завершает работу.")
