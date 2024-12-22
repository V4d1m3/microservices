from fastapi import HTTPException, Security
import httpx
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from logging import getLogger

DATABASE_SERVICE_URL = "http://db_service:8090"
AUTH_SERVICE_URL = "http://auth_service:8001/auth/verify-token"

security = HTTPBearer()
logger = getLogger(__name__)

async def get_current_user(authorization: HTTPAuthorizationCredentials = Security(security)):
    """
    Проверяет токен через сервис авторизации.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AUTH_SERVICE_URL,
                headers={"Authorization": f"Bearer {authorization.credentials}"}
            )
            if response.status_code != 200:
                logger.warning(f"Authorization failed: {response.json()}")
                raise HTTPException(status_code=401, detail="Invalid token")
            logger.info("User successfully authorized")
            return response.json()
    except httpx.RequestError as exc:
        logger.error(f"Authorization service unavailable: {exc}")
        raise HTTPException(status_code=503, detail="Authorization service unavailable")


async def get_announcements_by_user(user_id: int):
    """
    Получает список объявлений пользователя из базы данных.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{DATABASE_SERVICE_URL}/announcements/user/{user_id}")
            if response.status_code != 200:
                logger.warning(f"Announcements not found for user {user_id}: {response.json()}")
                raise HTTPException(status_code=response.status_code, detail="Announcements not found")
            logger.info(f"Announcements fetched for user {user_id}")
            return response.json()
    except httpx.RequestError as exc:
        logger.error(f"Database service unavailable while fetching announcements for user {user_id}: {exc}")
        raise HTTPException(status_code=503, detail="Database service unavailable")


async def get_announcements_by_type(item_type: bool):
    """
    Получает список объявлений из базы данных по типу.
    - `item_type`: True для найденных предметов, False для потерянных.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DATABASE_SERVICE_URL}/announcements/type/",
                params={"item_type": item_type}
            )
            if response.status_code != 200:
                logger.warning(f"Announcements of type {item_type} not found: {response.json()}")
                raise HTTPException(status_code=response.status_code, detail="Announcements not found")
            logger.info(f"Announcements of type {item_type} fetched successfully")
            return response.json()
    except httpx.RequestError as exc:
        logger.error(f"Database service unavailable while fetching announcements of type {item_type}: {exc}")
        raise HTTPException(status_code=503, detail="Database service unavailable")


async def get_responses_by_announcement(announcement_id: int):
    """
    Получает отклики на объявление из базы данных.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{DATABASE_SERVICE_URL}/responses/announcement/{announcement_id}")
            if response.status_code != 200:
                logger.warning(f"Responses not found for announcement {announcement_id}: {response.json()}")
                raise HTTPException(status_code=response.status_code, detail="Responses not found")
            logger.info(f"Responses fetched for announcement {announcement_id}")
            return response.json()
    except httpx.RequestError as exc:
        logger.error(f"Database service unavailable while fetching responses for announcement {announcement_id}: {exc}")
        raise HTTPException(status_code=503, detail="Database service unavailable")


async def get_responses_by_user(user_id: int):
    """
    Получает отклики пользователя из базы данных.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{DATABASE_SERVICE_URL}/responses/user/{user_id}")
            if response.status_code != 200:
                logger.warning(f"Responses not found for user {user_id}: {response.json()}")
                raise HTTPException(status_code=response.status_code, detail="Responses not found")
            logger.info(f"Responses fetched for user {user_id}")
            return response.json()
    except httpx.RequestError as exc:
        logger.error(f"Database service unavailable while fetching responses for user {user_id}: {exc}")
        raise HTTPException(status_code=503, detail="Database service unavailable")
