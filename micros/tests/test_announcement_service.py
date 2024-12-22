from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime

# Модели для тестирования
class AnnouncementCreate(BaseModel):
    user_id: int
    item: str
    place: str
    type: bool
    time: datetime = None

class AnnouncementResponse(BaseModel):
    announcement_id: int
    responding_user_id: int
    message: str
    time: datetime

# Пример приложения
app = FastAPI()

# Пример зависимости
async def get_current_user():
    return {"user_id": 1}

# Маршруты
@app.post("/announcements/")
async def create_announcement(
    announcement: AnnouncementCreate, user: dict = Depends(get_current_user)
):
    if not announcement.item or not announcement.place:
        raise HTTPException(status_code=400, detail="Invalid announcement data")
    return {"id": 1, "user_id": user["user_id"], "item": announcement.item, "place": announcement.place}

@app.get("/announcements/")
async def list_announcements():
    return [
        {"id": 1, "user_id": 1, "item": "Phone", "place": "Park", "type": False, "time": "2023-12-01T10:00:00"}
    ]

@app.get("/announcements/{announcement_id}")
async def get_announcement(announcement_id: int):
    if announcement_id != 1:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return {"id": 1, "user_id": 1, "item": "Phone", "place": "Park", "type": False, "time": "2023-12-01T10:00:00"}

@app.post("/responses/")
async def respond_to_announcement(
    response: AnnouncementResponse, user: dict = Depends(get_current_user)
):
    if not response.message or response.announcement_id != 1:
        raise HTTPException(status_code=400, detail="Invalid response data")
    return {"status": "success", "detail": "Response sent"}

# Клиент для тестирования
client = TestClient(app)

# Тесты
def test_create_announcement_success():
    """
    Успешное создание объявления.
    """
    response = client.post(
        "/announcements/",
        json={"user_id": 1, "item": "Wallet", "place": "Mall", "type": True, "time": "2023-12-01T10:00:00"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["item"] == "Wallet"

def test_create_announcement_invalid_data():
    """
    Создание объявления с пустыми данными.
    """
    response = client.post(
        "/announcements/",
        json={"user_id": 1, "item": "", "place": "", "type": True, "time": "2023-12-01T10:00:00"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid announcement data"

def test_list_announcements():
    """
    Получение списка объявлений.
    """
    response = client.get("/announcements/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["item"] == "Phone"

def test_get_announcement_success():
    """
    Успешное получение конкретного объявления.
    """
    response = client.get("/announcements/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["item"] == "Phone"

def test_get_announcement_not_found():
    """
    Получение несуществующего объявления.
    """
    response = client.get("/announcements/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Announcement not found"

def test_respond_to_announcement_success():
    """
    Успешный отклик на объявление.
    """
    response = client.post(
        "/responses/",
        json={"announcement_id": 1, "responding_user_id": 1, "message": "Found it!", "time": "2023-12-01T10:00:00"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_respond_to_announcement_invalid():
    """
    Отклик на несуществующее объявление или с пустым сообщением.
    """
    response = client.post(
        "/responses/",
        json={"announcement_id": 2, "responding_user_id": 1, "message": "", "time": "2023-12-01T10:00:00"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid response data"

