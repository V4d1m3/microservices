import logging
from fastapi import FastAPI
from routes import router
from prometheus_fastapi_instrumentator import Instrumentator

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    filename="report_service.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI(
    title="Report Service",
    description="Сервис для получения отчётов об объявлениях и ответах"
)

# Подключение маршрутов
app.include_router(router)

# Инструмент Prometheus для метрик
Instrumentator().instrument(app).expose(app)
