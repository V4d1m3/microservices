import logging
from fastapi import HTTPException, Security
from datetime import datetime
import httpx
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

DATABASE_SERVICE_URL = "http://db_service:8090"
AUTH_SERVICE_URL = "http://auth_service:8001/auth/verify-token"

security = HTTPBearer()
logger = logging.getLogger(__name__)


# Проверка текущего пользователя через Auth Service
async def get_current_user(authorization: HTTPAuthorizationCredentials = Security(security)):
    """
    Проверка токена и получение информации о пользователе.
    """
    logger.info("Verifying user token")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            AUTH_SERVICE_URL,
            headers={"Authorization": f"Bearer {authorization.credentials}"}
        )
        if response.status_code != 200:
            logger.error(f"Token verification failed: {response.status_code}")
            raise HTTPException(status_code=401, detail="Invalid token")

        logger.info("Token verified successfully")
        return response.json()


# Добавление объявления
async def add_announcement(user_id: int, announcement):
    """
    Добавление нового объявления в базу данных.
    """
    logger.info(f"Adding new announcement for user {user_id}: {announcement.dict()}")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DATABASE_SERVICE_URL}/announcements/",
            json={
                "user_id": user_id,
                "item": announcement.item,
                "place": announcement.place,
                "type": announcement.type,
                "time": announcement.time.isoformat() if announcement.time else None,
            },
        )
        if response.status_code != 200:
            logger.error(f"Failed to add announcement: {response.status_code}")
            raise HTTPException(status_code=500, detail="Failed to add announcement")
        announcement_id = response.json().get("id")
        logger.info(f"Announcement added successfully with ID: {announcement_id}")
        return announcement_id


# Получение всех объявлений
async def get_announcements():
    """
    Получение списка всех объявлений.
    """
    logger.info("Fetching all announcements from database")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DATABASE_SERVICE_URL}/announcements/")
        if response.status_code != 200:
            logger.error(f"Failed to fetch announcements: {response.status_code}")
            raise HTTPException(status_code=500, detail="Failed to fetch announcements")
        logger.info("Announcements fetched successfully")
        return response.json()


# Получение объявления по ID
async def get_announcement_by_id(announcement_id: int):
    """
    Получение информации об объявлении по его ID.
    """
    logger.info(f"Fetching announcement with ID {announcement_id}")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DATABASE_SERVICE_URL}/announcements/{announcement_id}")
        if response.status_code == 404:
            logger.error(f"Announcement not found: {announcement_id}")
            raise HTTPException(status_code=404, detail="Announcement not found")
        elif response.status_code != 200:
            logger.error(f"Failed to fetch announcement: {response.status_code}")
            raise HTTPException(status_code=500, detail="Failed to fetch announcement")
        logger.info(f"Announcement with ID {announcement_id} fetched successfully")
        return response.json()


# Ответ на объявление
async def respond_to_announcement(announcement_id: int, responding_user_id: int, message: str, time: datetime):
    """
    Сохранение ответа на объявление.
    """
    logger.info(f"Responding to announcement {announcement_id} by user {responding_user_id}")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DATABASE_SERVICE_URL}/responses/",
            json={
                "announcement_id": announcement_id,
                "responding_user_id": responding_user_id,
                "message": message,
                "time": time.isoformat(),
            }
        )
        if response.status_code == 404:
            logger.error(f"Announcement not found: {announcement_id}")
            raise HTTPException(status_code=404, detail="Announcement not found")
        elif response.status_code != 200:
            logger.error(f"Failed to respond to announcement: {response.status_code}")
            raise HTTPException(status_code=500, detail="Failed to respond to announcement")
        logger.info("Response to announcement saved successfully")
        return response.json()
