from sqlalchemy import select
from sqlalchemy.orm import joinedload, aliased
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings


    @classmethod
    async def find_by_user(cls, user_id):
        async with async_session_maker() as session:
            r = aliased(Rooms)
            b = aliased(Bookings)

            # For embedded structure
            # query = (select(cls.model)
            #          .filter(cls.model.user_id == user_id)
            #          .options(joinedload(cls.model.room).load_only(Rooms.image_id, 
            #                                                        Rooms.name, 
            #                                                        Rooms.description, 
            #                                                        Rooms.services))) #.load_only(Room.image_id, Room.name, Room.description, Room.services)

            # For flat structure
            query = (select(
                b.id,
                b.room_id,
                b.user_id,
                b.date_from,
                b.date_to,
                b.price,
                b.total_cost,
                b.total_days,
                r.image_id,
                r.name,
                r.description,
                r.services,
                )   
                     .filter(b.user_id==user_id)
                     .select_from(b)
                     .join(r, b.user_id == r.id, isouter=True)
                     )
            result = await session.execute(query)
            return result.mappings().all()

    