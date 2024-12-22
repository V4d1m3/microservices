import pytest
from fastapi import FastAPI, HTTPException, Depends
from fastapi.testclient import TestClient
from datetime import datetime
from pydantic import BaseModel

# Заглушки для схем
class ReportAnnouncementOut(BaseModel):
    id: int
    user_id: int
    item: str
    place: str
    time: datetime
    type: bool  # True = Найдено, False = Потеряно

class ReportResponseOut(BaseModel):
    id: int
    announcement_id: int
    responding_user_id: int
    message: str
    time: datetime

# Заглушка для проверки текущего пользователя
def get_current_user_stub():
    return {"user_id": 1}

# Заглушки для данных
mock_announcements = [
    {
        "id": 1,
        "user_id": 1,
        "item": "Phone",
        "place": "Park",
        "time": datetime.now(),
        "type": True,
    },
    {
        "id": 2,
        "user_id": 1,
        "item": "Wallet",
        "place": "Mall",
        "time": datetime.now(),
        "type": False,
    },
]

mock_responses = [
    {
        "id": 1,
        "announcement_id": 1,
        "responding_user_id": 2,
        "message": "I found your phone!",
        "time": datetime.now(),
    }
]

# Определение приложения и маршрутов
app = FastAPI()

@app.get("/reports/announcements/user/{user_id}", response_model=list[ReportAnnouncementOut])
async def get_user_announcements(user_id: int, user: dict = Depends(get_current_user_stub)):
    announcements = [ann for ann in mock_announcements if ann["user_id"] == user_id]
    if not announcements:
        raise HTTPException(status_code=404, detail="No announcements found")
    return announcements

@app.get("/reports/responses/announcement/{announcement_id}", response_model=list[ReportResponseOut])
async def get_responses_by_announcement(announcement_id: int, user: dict = Depends(get_current_user_stub)):
    responses = [resp for resp in mock_responses if resp["announcement_id"] == announcement_id]
    if not responses:
        raise HTTPException(status_code=404, detail="No responses found")
    return responses

# Клиент для тестирования
client = TestClient(app)

# Тесты
def test_get_user_announcements_success():
    response = client.get("/reports/announcements/user/1")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_user_announcements_not_found():
    response = client.get("/reports/announcements/user/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "No announcements found"

def test_get_responses_by_announcement_success():
    response = client.get("/reports/responses/announcement/1")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_responses_by_announcement_not_found():
    response = client.get("/reports/responses/announcement/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "No responses found"
