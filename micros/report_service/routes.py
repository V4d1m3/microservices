import logging
from fastapi import APIRouter, Depends, HTTPException
from schemas import ReportAnnouncementOut, ReportResponseOut
from utils import (
    get_current_user,
    get_announcements_by_user,
    get_announcements_by_type,
    get_responses_by_announcement,
    get_responses_by_user
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/announcements/user/{user_id}", response_model=list[ReportAnnouncementOut])
async def get_user_announcements(user_id: int, user: dict = Depends(get_current_user)):
    """
    Эндпоинт для получения объявлений пользователя.
    """
    logger.info(f"Fetching announcements for user {user_id}")
    try:
        announcements = await get_announcements_by_user(user_id)
        if not announcements:
            logger.warning(f"No announcements found for user {user_id}")
            raise HTTPException(status_code=404, detail="No announcements found")
        logger.info(f"Successfully fetched announcements for user {user_id}")
        return announcements
    except HTTPException as e:
        logger.error(f"Error fetching announcements for user {user_id}: {e.detail}")
        raise


@router.get("/announcements/type", response_model=list[ReportAnnouncementOut])
async def get_announcements_by_type_router(
    item_type: bool, user: dict = Depends(get_current_user)
):
    """
    Эндпоинт для получения объявлений по типу.
    """
    logger.info(f"Fetching announcements of type {item_type}")
    try:
        announcements = await get_announcements_by_type(item_type)
        if not announcements:
            logger.warning(f"No announcements found for type {item_type}")
            raise HTTPException(status_code=404, detail="No announcements found")
        logger.info(f"Successfully fetched announcements for type {item_type}")
        return announcements
    except HTTPException as e:
        logger.error(f"Error fetching announcements of type {item_type}: {e.detail}")
        raise


@router.get("/responses/announcement/{announcement_id}", response_model=list[ReportResponseOut])
async def get_responses_by_announcement_router(
    announcement_id: int, user: dict = Depends(get_current_user)
):
    """
    Эндпоинт для получения откликов на объявление.
    """
    logger.info(f"Fetching responses for announcement {announcement_id}")
    try:
        responses = await get_responses_by_announcement(announcement_id)
        if not responses:
            logger.warning(f"No responses found for announcement {announcement_id}")
            raise HTTPException(status_code=404, detail="No responses found")
        logger.info(f"Successfully fetched responses for announcement {announcement_id}")
        return responses
    except HTTPException as e:
        logger.error(f"Error fetching responses for announcement {announcement_id}: {e.detail}")
        raise


@router.get("/responses/user/{user_id}", response_model=list[ReportResponseOut])
async def get_responses_by_user_router(
    user_id: int, user: dict = Depends(get_current_user)
):
    """
    Эндпоинт для получения откликов пользователя.
    """
    logger.info(f"Fetching responses for user {user_id}")
    try:
        responses = await get_responses_by_user(user_id)
        if not responses:
            logger.warning(f"No responses found for user {user_id}")
            raise HTTPException(status_code=404, detail="No responses found")
        logger.info(f"Successfully fetched responses for user {user_id}")
        return responses
    except HTTPException as e:
        logger.error(f"Error fetching responses for user {user_id}: {e.detail}")
        raise

