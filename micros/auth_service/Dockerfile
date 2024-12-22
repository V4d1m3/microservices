FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Скопируем только requirements.txt для предварительной установки зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное приложение
COPY . .

# Команда запуска приложения
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]
