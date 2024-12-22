import json
import logging

# Настройка логгера
logger = logging.getLogger(__name__)


def process_notification(body):
    """
    Обработка уведомления из очереди RabbitMQ.
    """
    try:
        message = json.loads(body)
        user_id = message.get("user_id")
        content = message.get("content")

        if not user_id or not content:
            raise ValueError("Missing required fields: 'user_id' or 'content'")

        logger.info(f"[Notification] User ID: {user_id}, Content: {content}")
        # Здесь можно добавить логику отправки уведомлений (например, на email или push-сообщения)

    except json.JSONDecodeError:
        logger.error("Failed to decode message: Invalid JSON format")
    except ValueError as ve:
        logger.error(f"Invalid message structure: {ve}")
    except Exception as e:
        logger.error(f"Failed to process notification: {e}", exc_info=True)
