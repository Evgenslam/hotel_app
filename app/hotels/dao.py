from datetime import date

from sqlalchemy import and_, func, select, DATE, cast, Integer, text
from sqlalchemy.orm import aliased, selectinload, joinedload

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.rooms.models import Rooms
from app.database import async_session_maker


class HotelDAO(BaseDAO):
    model = Hotels


    @classmethod

    # INCORRECT
    async def find_available_hotels_selectin(cls, 
                                    location: str,
                                    date_from: date,
                                    date_to: date):
        async with async_session_maker() as session:

            r = aliased(Rooms)
            b = aliased(Bookings)
            h = aliased(Hotels)

            # subq = (select(b).filter 
            # (and_(
            #         b.date_from <= date_to,
            #         b.date_to >= date_from)))

            # rb stands for room bookings. Here we get number of bookings per hotel in the specified days
            rb = (select(r.hotel_id, func.count().label("booked_rooms"))
                            .select_from(r)
                            .join(b, r.id == b.room_id)
                            .group_by(r.hotel_id)
                            .filter(
                                b.date_from <= date_to,
                                b.date_to >= date_from))
            
    

            # Construct a query to fetch Hotels and eager load their rooms
            query = (
                select(cls.model)
                .options(selectinload(cls.model.rooms).selectinload(rb))
                .filter(cls.model.location.contains(location))
            )

            # Execute the query
            res = await session.execute(query)
            return res.mappings().all() #[x.rooms for x in res.scalars().all()]  


    @classmethod
    async def find_available_hotels(cls, 
                                    location: str,
                                    date_from: date,
                                    date_to: date):
        async with async_session_maker() as session:

        
            r = aliased(Rooms)
            b = aliased(Bookings)
            h = aliased(Hotels)

            # bfd stands for booking for dates. We first get only bookings that overlap with dates we get
            bfd = (select(b).filter 
            (and_(
   
                    b.date_from <= date_to,
                    b.date_to >= date_from)
                    )).cte("bfd")
            
            # rb stands for room bookings. Here we get number of bookings per hotel in the specified days
            rb = (select(r.hotel_id, func.count().label("booked_rooms"))
                            .select_from(r)
                            .join(bfd, r.id == bfd.c.room_id)
                            .group_by(r.hotel_id)).cte("rb")
            
            # finally we get hotels with rooms_left column
            query = (select(
                h.id, 
                h.name,
                h.location, 
                h.services, 
                h.rooms_quantity, 
                h.image_id, 
                (h.rooms_quantity - func.coalesce(rb.c.booked_rooms, 0)).label("rooms_left"))
                .select_from(h)
                .join(rb, h.id == rb.c.hotel_id, isouter=True)
                .filter(
                    h.location.contains(location), 
                    (h.rooms_quantity - func.coalesce(rb.c.booked_rooms, 0)) > 0      
                ))
                        
            res = await session.execute(query)
            return res.mappings().all()


        """"
        RAW SQL 

        WITH BookingsForDates AS (
        SELECT *
        FROM bookings
        WHERE date_from <= '2023-06-27' 
            AND date_to >= '2023-06-25'
        ),
        RoomBookings AS (
            SELECT r.hotel_id, COUNT(*) AS booked_rooms
            FROM rooms r
            JOIN BookingsForDates bfd ON r.id = bfd.room_id
            GROUP BY r.hotel_id
        )
        SELECT h.*, 
            (h.rooms_quantity - COALESCE(rb.booked_rooms, 0)) AS rooms_left
            FROM hotels h
            LEFT JOIN RoomBookings rb ON h.id = rb.hotel_id
            WHERE h.location LIKE '%Алтай%'
	            AND (h.rooms_quantity - COALESCE(rb.booked_rooms, 0)) > 0;
        """


    @classmethod
    async def get_rooms_by_hotel(cls, 
                                 hotel_id: str,
                                 date_from: date,
                                 date_to: date):
        async with async_session_maker() as session:

            r = aliased(Rooms)
            b = aliased(Bookings)
            h = aliased(Hotels)
            
            # relbook stands for relevant bookings. Here we get number of bookings per room (roomtype?) in the specified days
            relbook = (select(
                r.id,
                func.count().label("booked_rooms"))
                .select_from(r)
                .join(b, r.id == b.room_id)
                .filter(
                    b.date_from <= date_to,
                    b.date_to >= date_from
                )
                .group_by(r.id)
                ).cte("rb")
            
            # relhot stands for relevant hotels. Here we get the hotel with the specified id
            relhot = (select(h)
            .select_from(h)
            .filter(h.id == hotel_id)
            ).cte("rh")

            # Here we can see what SQL query is compiled
            print("RB SQL")
            print(relbook.compile(compile_kwargs={"literal_binds": True}))
            
            query = (select(
                relhot.c.id.label("hotel_id"),
                r.id,
                r.name,
                r.description,
                r.services,
                r.price,
                r.quantity,
                r.image_id,
                ((date_to - date_from).days * r.price).label("total_cost"),  
                (r.quantity - func.coalesce(relbook.c.booked_rooms, 0)).label("rooms_left"))
            .select_from(relhot)
            .join(r, relhot.c.id == r.hotel_id)
            .join(relbook, r.id == relbook.c.id, isouter=True))

            res = await session.execute(query)

            # Here we can see what SQL query is compiled
            print("Query SQL")
            print(query.compile(compile_kwargs={"literal_binds": True}))

            return res.mappings().all()

        """
        RAW SQL 
        
        WITH RoomBookings AS (
        SELECT r.id, COUNT(*) AS booked_rooms
        FROM rooms r
        JOIN bookings b ON r.id = b.room_id
        WHERE date_from <= '2023-06-27' 
            AND date_to >= '2023-06-25'
        GROUP BY r.id
),      
       
        RelevantHotels AS(
        SELECT *
		FROM hotels h
        WHERE h.id = 3
        )


        SELECT 
            rh.id AS hotel_id, 
            r.id AS room_id,
            r.name,
            r.description,
            r.services,
            r.price,
            r.quantity,
            r.image_id,
            ((CAST('2023-06-27' AS DATE) - CAST('2023-06-25' AS DATE)) * r.price) AS total_cost,
            (r.quantity - COALESCE(rb.booked_rooms, 0)) AS rooms_left
        FROM 
            RelevantHotels rh
        JOIN 
            rooms r ON rh.id = r.hotel_id
        LEFT JOIN
            RoomBookings rb ON r.id = rb.id;
        """
