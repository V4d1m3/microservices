from datetime import datetime, timezone
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String
)
from sqlalchemy.orm import relationship
from database import Base


# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Связь с объявлениями и ответами
    announcements = relationship("Announcement", back_populates="user")
    responses = relationship("Response", back_populates="responding_user")


# Модель объявления о потерянном или найденном предмете
class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item = Column(String, nullable=False)  # Название предмета
    place = Column(String, nullable=False)  # Место, где найдено/потеряно
    time = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    type = Column(Boolean, nullable=False)  # True = Найдено, False = Потеряно

    # Связь с пользователем и ответами
    user = relationship("User", back_populates="announcements")
    responses = relationship("Response", back_populates="announcement")


# Модель ответа на объявление
class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, ForeignKey("announcements.id"), nullable=False)
    responding_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)  # Сообщение от пользователя
    time = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Связь с объявлением и пользователем
    announcement = relationship("Announcement", back_populates="responses")
    responding_user = relationship("User", back_populates="responses")
