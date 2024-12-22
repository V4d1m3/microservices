from pydantic import BaseModel
from datetime import datetime

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
