from fastapi import APIRouter
from datetime import date
from inspect import getfullargspec
from app.hotels.models import Hotels
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SAvailableHotel, SHotel
from app.rooms.schemas import SAvailableRoom, SHotelWithRooms
from inspect import signature 


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)

filters = {"price": 4300}

@router.get("")
async def get_hotels(
    location: str,
    date_from: date,
    date_to: date) -> list[SAvailableHotel]:

    res = await HotelDAO.find_available_hotels(location, date_from, date_to)
    return res


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel(
    hotel_id: int,
    date_from: date,
    date_to: date) -> list[SAvailableRoom]:

    res = await HotelDAO.get_rooms_by_hotel(hotel_id, date_from, date_to)
    return res

"""
Пример эндпоинта: /hotels/1/rooms.
HTTP метод: GET.
HTTP код ответа: 200.
Описание: возвращает список всех номеров определенного отеля.
Нужно быть авторизованным: нет.
Параметры: параметр пути hotel_id и параметры запроса date_from, date_to.
Ответ пользователю: для каждого номера должно быть указано: 
id, hotel_id, name, description, services, price, quantity, image_id, total_cost (стоимость бронирования номера за весь период), 
rooms_left (количество оставшихся номеров).
"""


@router.get("/id/{hotel_id}")
async def get_rooms_by_hotel(hotel_id: int) -> SHotel:
    id_filter = {"id": hotel_id}
    res = await HotelDAO.find_one_or_none(**id_filter)
    return res
    
"""
Пример эндпоинта: /hotels/id/1.
HTTP метод: GET.
HTTP код ответа: 200.
Описание: возвращает все данные по одному отелю.
Нужно быть авторизованным: нет.
Параметры: параметр пути hotel_id.
Ответ пользователю: для отеля должно быть указано: id, name, location, services, rooms_quantity, image_id 
    
"""




