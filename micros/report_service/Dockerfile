FROM python:3.12-slim

# Устанавливаем системные зависимости (при необходимости)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями для кэширования установки
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копируем оставшийся код приложения
COPY . .

# Устанавливаем команду запуска
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8044"]
