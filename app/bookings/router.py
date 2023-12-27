from fastapi import APIRouter
from sqlalchemy import select
from app.bookings.models import Bookings
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingWithRoomInfo


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_by_user(user_id: int)-> list[SBookingWithRoomInfo]:
    return await BookingDAO.find_by_user(user_id)

@router.get("/get/{booking_id}")
async def get_booking(booking_id: int):
    return await BookingDAO.find_by_id(booking_id)

@router.delete("/{booking_id}")
async def delete_booking(booking_id: int):
    booking_id_filter = {"id": booking_id}
    return await BookingDAO.delete(**booking_id_filter)


"""
I deleted this booking:

{
  "room_id": 7,
  "id": 2,
  "total_days": 15,
  "user_id": 2,
  "date_from": "2023-06-25",
  "date_to": "2023-07-10",
  "price": 4300,
  "total_cost": 64500
}
"""