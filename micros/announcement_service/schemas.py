from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Создание объявления
class AnnouncementCreate(BaseModel):
    user_id: int
    item: str  # Название предмета
    place: str  # Место, где найдено/потеряно
    type: bool  # True = Найдено, False = Потеряно
    time: Optional[datetime] = None


# Полная информация об объявлении
class AnnouncementOut(BaseModel):
    id: int
    user_id: int
    item: str
    place: str
    time: datetime
    type: bool

    class Config:
        orm_mode = True


# Ответ на объявление
class AnnouncementResponse(BaseModel):
    announcement_id: int
    responding_user_id: int
    message: str  # Сообщение от пользователя
    time: datetime

    class Config:
        orm_mode = True


# Модель для сообщения в Notification Service
class NotificationMessage(BaseModel):
    user_id: int
    responding_user_id: int
    announcement_id: int
    content: str  # Сообщение для уведомления


# Ответ с подтверждением действия
class ActionResponse(BaseModel):
    status: str
    detail: Optional[str] = None
