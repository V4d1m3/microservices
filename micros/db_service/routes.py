from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime
from database import get_db

# Маршруты для пользователей
users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = models.User(
        username=user.username,
        hashed_password=user.hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@users_router.get("/", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.get("/by-username/", response_model=schemas.UserOut)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Маршруты для объявлений
announcements_router = APIRouter(prefix="/announcements", tags=["Announcements"])

@announcements_router.post("/", response_model=schemas.AnnouncementOut)
def create_announcement(data: schemas.AnnouncementCreate, db: Session = Depends(get_db)):
    new_announcement = models.Announcement(
        user_id=data.user_id,
        item=data.item,
        place=data.place,
        type=data.type,
        time=data.time or datetime.now()
    )
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return new_announcement

@announcements_router.get("/{announcement_id}", response_model=schemas.AnnouncementOut)
def get_announcement(announcement_id: int, db: Session = Depends(get_db)):
    announcement = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return announcement

@announcements_router.get("/", response_model=list[schemas.AnnouncementOut])
def list_announcements(db: Session = Depends(get_db)):
    announcements = db.query(models.Announcement).all()
    return announcements

@announcements_router.get("/user/{user_id}", response_model=list[schemas.AnnouncementOut])
def get_announcements_by_user(user_id: int, db: Session = Depends(get_db)):
    announcements = db.query(models.Announcement).filter(models.Announcement.user_id == user_id).all()
    if not announcements:
        raise HTTPException(status_code=404, detail="No announcements found for this user")
    return announcements

@announcements_router.get("/type/", response_model=list[schemas.AnnouncementOut])
def get_announcements_by_type(item_type: bool, db: Session = Depends(get_db)):
    """
    Получить объявления по типу:
    - `True` = Найденные предметы
    - `False` = Потерянные предметы
    """
    announcements = db.query(models.Announcement).filter(models.Announcement.type == item_type).all()
    return announcements

# Маршруты для ответов на объявления
responses_router = APIRouter(prefix="/responses", tags=["Responses"])

@responses_router.post("/", response_model=schemas.ResponseOut)
def create_response(data: schemas.ResponseCreate, db: Session = Depends(get_db)):
    """
    Создать отклик на объявление.
    """
    # Проверяем, существует ли объявление
    announcement = db.query(models.Announcement).filter(models.Announcement.id == data.announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    # Проверяем, существует ли пользователь, отправляющий отклик
    user = db.query(models.User).filter(models.User.id == data.responding_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Responding user not found")

    # Создаем новый отклик
    new_response = models.Response(
        announcement_id=data.announcement_id,
        responding_user_id=data.responding_user_id,
        message=data.message,
        time=data.time or datetime.now()
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return new_response

@responses_router.get("/announcement/{announcement_id}", response_model=list[schemas.ResponseOut])
def get_responses_by_announcement(announcement_id: int, db: Session = Depends(get_db)):
    """
    Получить все отклики на конкретное объявление.
    """
    responses = db.query(models.Response).filter(models.Response.announcement_id == announcement_id).all()
    if not responses:
        raise HTTPException(status_code=404, detail="No responses found for this announcement")
    return responses

@responses_router.get("/user/{user_id}", response_model=list[schemas.ResponseOut])
def get_responses_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получить все отклики, сделанные конкретным пользователем.
    """
    responses = db.query(models.Response).filter(models.Response.responding_user_id == user_id).all()
    if not responses:
        raise HTTPException(status_code=404, detail="No responses found for this user")
    return responses
