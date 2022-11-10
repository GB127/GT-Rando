from generic import RandomizerError, world_indexes, room_to_index, LogicError
from items import Items
from exits import Exits
import matplotlib.pyplot as plt
import networkx as net # version 2.5

class World():
    def __init__(self, data, world_i):
        self.world_i = world_i
        self.data = data
        self.screens = world_indexes(self.world_i)

        self.Exits = Exits(self.data,self.world_i,self.screens)
        self.Items = Items(self.data, self.world_i, self.screens)


    def __call__(self):
        self.Exits(randomize=True, keep_direction=True, pair_exits=True)
        self.Items(randomize_items=True)
        self.nodes()


    def nodes(self):
        g = net.compose(self.Exits.nodes(), self.Items.nodes(self.Exits))
        return g


    def __getitem__(self, screen):
        return {"exits":self.Exits[screen], "items":self.Items[screen]}
