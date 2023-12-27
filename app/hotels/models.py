from app.database import Base
from sqlalchemy import JSON, Column, Computed, Integer, String, func
from sqlalchemy.orm import relationship, mapped_column, Mapped


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    #rooms_left: Mapped[int] = mapped_column(Computed("room_quantity - "))
    image_id: Mapped[int]

    rooms = relationship("Rooms", back_populates="hotel")
   