from os import access
from generic import world_indexes, room_to_index
from items import Items
from exits import Exits
import matplotlib.pyplot as plt
import networkx as net # version 2.5

class World():
    def __init__(self, data, world_i):
        self.world_i = world_i
        self.data = data

        self.Exits = Exits(self.data,self.world_i, world_indexes(self.world_i))
        self.Items = Items(self.data, self.world_i, world_indexes(self.world_i))

    def __call__(self):
        compte = 0
        while True:

            try:
                compte += 1
                self.Items(randomize_items=True, randomize_fruits=True, combine=True)

                [self.logic_0][self.world_i]()
                break
            except:
                pass
            if compte == 9:
                raise BaseException()


    def logic_0(self):
        def preparation():
                # remove locked door.
            g.remove_edge(8, 5)
            g.remove_edge(5, 8)
            # Plank
            for sortie in self[7]["exits"][:2]:
                g.remove_edge(7, sortie.destination)
                g.remove_edge(sortie.destination, 7)

        def unlock_door():
            g.add_edge(8,5)
            g.add_edge(5,8)
            used.append(0xA)
        
        def use_plank():
            for sortie in self[7]["exits"][:2]:
                g.add_edge(7, sortie.destination)
                g.add_edge(sortie.destination, 7)

            used.append(0xE)

        def available_items():
            progression = {0xA : "Grey Key",0xB : "Gold Key", 0xE : "Bridge"}

            toreturn = []
            for screen in net.shortest_path(g, 0):
                if screen == 7:
                    continue
                toreturn += [x for x in self[screen]["items"] if x in progression]

            for screen in net.shortest_path(g,0):
                for sortie in self[screen]["exits"]:
                    if sortie.destination == 7 and sortie.spawn == "W":
                        toreturn += [x for x in self[7]["items"] if x in progression]
                    elif sortie.destination == 9 and sortie.spawn == "S":
                        toreturn += [x for x in self[9]["items"] if x in progression]

            for used_item in used:
                toreturn.remove(used_item)
            return toreturn

        def available_actions():
            actions = []
            for screen in net.shortest_path(g, 0).keys():
                for sortie in self[screen]["exits"]:
                    if sortie.destination == 7 and sortie.spawn in ["N","S"]:
                        if 14 in available_items():
                            actions.append(use_plank)

            if 5 in net.shortest_path(g, 0).keys() or 8 in net.shortest_path(g, 0).keys():
                if 0xA in available_items():
                    actions.append(unlock_door)
            return actions

        g = self.Exits.nodes()
        preparation()
        used = []

        # With these two things, if both 2 passes, I then know for sure that all levels are accessible.
        for _ in range(2):  # There is only two progression items. So I can simply do that.
            available_actions()[0]()
        g.clear()


    def __getitem__(self, B7):
        return {"exits":self.Exits[room_to_index(tup=(self.world_i, B7))], "items":self.Items[B7]}
