from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# Модель для создания пользователя
class UserCreate(BaseModel):
    username: str
    hashed_password: str

# Модель для отображения пользователя
class UserOut(BaseModel):
    id: int
    username: str
    hashed_password: str

# Модель для создания объявления о находке/потере предмета
class AnnouncementCreate(BaseModel):
    user_id: int
    item: str
    place: str
    type: bool  # True = Найдено, False = Потеряно
    time: Optional[datetime] = None

# Модель для ответа с информацией об объявлении
class AnnouncementOut(BaseModel):
    id: int
    user_id: int
    item: str
    place: str
    time: datetime
    type: bool  # True = Найдено, False = Потеряно



# Модель для создания отклика на объявление
class ResponseCreate(BaseModel):
    announcement_id: int
    responding_user_id: int
    message: str
    time: Optional[datetime] = None

# Модель для ответа с информацией об отклике
class ResponseOut(BaseModel):
    id: int
    announcement_id: int
    responding_user_id: int
    message: str
    time: datetime
