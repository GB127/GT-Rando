from generic import world_indexes, room_to_index
from items import Items
from exits import Exits

class World():
    def __init__(self, data, world_i):
        self.world_i = world_i
        self.data = data

        self.Exits = Exits(self.data,self.world_i, world_indexes(self.world_i))
        self.Items = Items(self.data, self.world_i, world_indexes(self.world_i))


