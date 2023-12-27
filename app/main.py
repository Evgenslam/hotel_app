from pydantic import BaseModel, Field
from datetime import date
from fastapi import FastAPI, Query
from typing import Optional

from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels

app = FastAPI()
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)



# @app.get("/hotels", response_model=list[SHotel])
# def get_hotels(
#     location: str,
#     date_from: date,
#     date_to: date,
#     stars: Optional[int] = Query(None, ge=1, le=6),
#     has_geisha: Optional[bool] = None
# ):
#     hotels = [
#         {
#             "address": "Улица Пушкина Дом Колотушкина",
#             "name": "abr yebyot Bobra",
#             "stars": 3
#         }
#     ]
#     return hotels

# @app.post("/bookings")
# def add_booking(booking: SBooking):
#     pass