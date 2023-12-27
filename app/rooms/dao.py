from app.dao.base import BaseDAO
from app.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms