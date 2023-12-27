from pydantic import BaseModel
from datetime import date

class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int


class SAvailableRoom(SRoom):
    total_cost: int
    rooms_left: int


class SRoomWithoutHotelID(BaseModel):
    id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int


class SHotelWithRooms(BaseModel):
    hotel_id: int
    rooms: list[SRoomWithoutHotelID]
   

   