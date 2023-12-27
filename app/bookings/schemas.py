from pydantic import BaseModel, Field
from datetime import date

class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

class SBookingWithRoomInfo(SBooking):
    id: int = Field(..., exclude=True)
    image_id: int
    name: str
    description: str
    services: list[str]
    
