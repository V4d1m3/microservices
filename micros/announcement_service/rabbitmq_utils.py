import pika
import json
import logging
import os

# Константы для подключения к RabbitMQ (можно переопределять через переменные окружения)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME", "notifications")

# Настройка логгера
logger = logging.getLogger(__name__)


def publish_message(message: dict):
    """
    Публикует сообщение в очередь RabbitMQ.
    :param message: Словарь с данными сообщения.
    """
    logger.info("Connecting to RabbitMQ...")

    connection = None
    try:
        # Устанавливаем соединение с RabbitMQ
        parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Объявляем очередь, если она не существует
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        logger.info(f"Queue '{QUEUE_NAME}' declared successfully.")

        # Публикуем сообщение
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  # Сообщения помечаются как "устойчивые" (persistent)
            )
        )
        logger.info(f"[RabbitMQ] Message sent to queue '{QUEUE_NAME}': {message}")

    except pika.exceptions.AMQPConnectionError as conn_err:
        logger.error(f"[RabbitMQ] Connection error: {conn_err}")
    except Exception as e:
        logger.error(f"[RabbitMQ] Unexpected error while publishing message: {e}")
    finally:
        # Закрываем соединение, если оно было установлено
        if connection and not connection.is_closed:
            try:
                connection.close()
                logger.info("RabbitMQ connection closed.")
            except Exception as close_err:
                logger.error(f"Error closing RabbitMQ connection: {close_err}")
