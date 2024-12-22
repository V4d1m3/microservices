FROM python:3.12-slim

# Устанавливаем системные зависимости (если нужны для RabbitMQ или других библиотек)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями отдельно для кэширования слоя
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копируем оставшийся код приложения
COPY . .

# Устанавливаем переменные среды
ENV PYTHONUNBUFFERED=1

# Устанавливаем команду запуска
CMD ["python", "main.py"]
