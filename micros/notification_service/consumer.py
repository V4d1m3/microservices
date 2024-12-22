import time
import pika
from pika import exceptions
import logging
from notifications import process_notification

# Конфигурация RabbitMQ
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "notifications"

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    """
    Callback-функция для обработки сообщений из RabbitMQ.
    """
    try:
        logger.info(f"Received message from queue '{QUEUE_NAME}'")
        process_notification(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Подтверждаем обработку сообщения
        logger.info("Message processed and acknowledged.")
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)


def start_consumer():
    """
    Запуск потребителя RabbitMQ.
    """
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=5672)

    while True:
        try:
            logger.info("Connecting to RabbitMQ...")

            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            # Объявляем устойчивую очередь
            channel.queue_declare(queue=QUEUE_NAME, durable=True)

            # Начинаем прослушивать очередь
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
            logger.info(f"Waiting for messages in queue '{QUEUE_NAME}'. To exit press CTRL+C")

            channel.start_consuming()
        except exceptions.AMQPConnectionError:
            logger.warning("RabbitMQ is not available. Retrying in 3 seconds...")
            time.sleep(3)
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            time.sleep(3)
