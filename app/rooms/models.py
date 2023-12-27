from typing import Optional
from app.database import Base
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]

    hotel = relationship("Hotels", back_populates="rooms")
    bookings = relationship("Bookings", back_populates="room")
    



   