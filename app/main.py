from pydantic import BaseModel, Field
from datetime import date
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()


class SHotel(BaseModel):
    address: str = Field(max_length=400)
    name: str
    stars: int 


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    


@app.get("/hotels", response_model=list[SHotel])
def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    stars: Optional[int] = Query(None, ge=1, le=6),
    has_geisha: Optional[bool] = None
):
    hotels = [
        {
            "address": "Улица Пушкина Дом Колотушкина",
            "name": "abr yebyot Bobra", 
            "stars": 3
        }
    ]
    return hotels

@app.post("/bookings")
def add_booking(booking: SBooking):
    pass