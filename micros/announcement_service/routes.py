import logging
from fastapi import APIRouter, HTTPException, Depends
from schemas import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementOut,
    NotificationMessage,
    ActionResponse
)
from rabbitmq_utils import publish_message
from utils import (
    get_current_user,
    add_announcement,
    get_announcements,
    get_announcement_by_id,
    respond_to_announcement
)

logger = logging.getLogger(__name__)

# Маршрутизаторы для объявлений и откликов
announcements_router = APIRouter(prefix="/announcements", tags=["Announcements"])
responses_router = APIRouter(prefix="/responses", tags=["Responses"])

# Эндпоинт для создания объявления
@announcements_router.post("/", response_model=ActionResponse)
async def create_announcement(
    announcement: AnnouncementCreate,
    user: dict = Depends(get_current_user)
):
    """
    Создание нового объявления.
    """
    logger.info(f"User {user['user_id']} is creating an announcement: {announcement.item}")
    try:
        announcement_id = await add_announcement(user_id=user["user_id"], announcement=announcement)
        logger.info(f"Announcement created with ID: {announcement_id}")
        return {"status": "success", "detail": f"Announcement created with ID {announcement_id}"}
    except Exception as e:
        logger.error(f"Failed to create announcement: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create announcement")


# Эндпоинт для получения всех объявлений
@announcements_router.get("/", response_model=list[AnnouncementOut])
async def list_announcements():
    """
    Получение всех объявлений.
    """
    logger.info("Fetching all announcements")
    try:
        announcements = await get_announcements()
        return announcements
    except Exception as e:
        logger.error(f"Failed to fetch announcements: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch announcements")


# Эндпоинт для получения одного объявления по ID
@announcements_router.get("/{announcement_id}", response_model=AnnouncementOut)
async def get_announcement(announcement_id: int):
    """
    Получение конкретного объявления по ID.
    """
    logger.info(f"Fetching announcement with ID {announcement_id}")
    try:
        announcement = await get_announcement_by_id(announcement_id)
        if not announcement:
            raise HTTPException(status_code=404, detail="Announcement not found")
        return announcement
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch announcement: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch announcement")


# Эндпоинт для ответа на объявление
@responses_router.post("/", response_model=ActionResponse)
async def respond_to_ann(
    response: AnnouncementResponse,
    user: dict = Depends(get_current_user)
):
    """
    Ответ на существующее объявление.
    """
    logger.info(
        f"User {user['user_id']} is responding to announcement {response.announcement_id} "
        f"with message: {response.message}"
    )

    try:
        # Проверка и сохранение ответа
        success = await respond_to_announcement(
            announcement_id=response.announcement_id,
            responding_user_id=user["user_id"],
            message=response.message,
            time=response.time
        )

        if not success:
            raise HTTPException(status_code=404, detail="Announcement not found")

        # Публикация уведомления через RabbitMQ
        notification = NotificationMessage(
            user_id=response.announcement_id,  # ID автора объявления
            responding_user_id=user["user_id"],
            announcement_id=response.announcement_id,
            content=f"User {user['user_id']} responded to your announcement: {response.message}"
        )
        publish_message(notification.dict())

        logger.info(f"User {user['user_id']} successfully responded to announcement {response.announcement_id}")
        return {"status": "success", "detail": "Response sent and notification published"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to respond to announcement: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to respond to announcement")

