from exits import Exits
from gameclass import GT
import random
from generic import world_indexes, room_to_index
from world import World
import networkx as net # version 2.5
import matplotlib.pyplot as plt
from items import Items



class debug(GT):
    def __init__(self, data):
        super().__init__(data)
        del self.Worlds
        self.Worlds = [World_debug(self.data, x) for x in range(5)]

    def save(self):
        super().save("debug.smc")

class World_debug(World):
    def screen_str(self, B7):
        def transform_byt_co(big_value):
            assert big_value <= 0x6bc and big_value >=0, "Byte value must be 0 to 0x6BC"
            assert big_value % 2 == 0, "Byte value must be pair, else it will appear gliched."

            y = ( big_value // 0x40) / 2
            x = (big_value % 0x40) / 2
            return x/2, y

        def get_interactives(screen_id):
            screen_data = self.data.screens[screen_id]
            interactives = []
            for id in range(screen_data.num_itiles):
                objet = screen_data.itiles[id]
                interactives.append((objet.type, transform_byt_co(objet.tile_index)))
            return interactives


        screen_id = room_to_index(tup=(self.world_i, B7))


        interactives_string = {
            0x0 : "W",
            0x2 : "A",
            0x4 : "E",
            0x6 : "S",
            0x8 : "P",
            0xA : "B",
            0xC : "L",
            0xE : "2",
            0x10 : "I",
            0x12 : "C",
            0x14 : "T",
            0x16 : "R",
            0x18 : "r",
            0x1A : "X",
            0x1C : "G",
            0x1E : "O",
            0x20 : "R"
            }

        boundary_top = "_" * 34
        boundary_bottom = "¯" * 34


        string_list = []
        for y in range(28):
            tempo = [" " for _ in range(32)]
            # ...
            for interactive in get_interactives(screen_id):
                typ = interactive[0]
                inter_x = interactive[1][0]
                inter_y = interactive[1][1] 
                if 2* inter_y == y or (2 * inter_y +1) == y:
                    tempo[int(2 * inter_x)] = interactives_string[typ]
                    tempo[int(2* inter_x) + 1] = interactives_string[typ]


            new_str = "|" + "".join(tempo) + "|"
            string_list.append(new_str)

        print(boundary_top)
        print("\n".join(string_list))
        print(boundary_bottom)

    def __init__(self, data, world_i):
        self.world_i = world_i
        self.data = data
        self.screens = world_indexes(self.world_i)

        self.Exits = Exits_debug(self.data,self.world_i, self.screens)
        self.Items = Items_debug(self.data, self.world_i, self.screens)


    def nodes(self,simplified=False, save:bool=False,*, planar=False, spectral=False, spring=False):
        def filename():
            string = f"Graph-{self.world_i}"
            return string + ".png"

        g = super().nodes()
        if save:
            color_map = []
            for node in g:
                if node[1] in ["Hookshot", "Grey Key", "Gold Key", "Bridge"]:
                    color_map.append("lightgreen")
                else:
                    color_map.append("yellow")
            net.draw(g, with_labels=True, node_color=color_map)
            plt.savefig(filename(), format="PNG")
            plt.clf()
            g.clear()
        return g




class Items_debug(Items):
    def nodes(self,exits, save:bool=False,*,simplified=False, planar=False, spectral=False, spring=False):
        def filename():
            string = f"Graph-{self.world_i}_items"
            if simplified:
                string += "_simplified"
            return string + ".png"
        g = super().nodes(exits)
        if save:
            color_map = []
            for node in g:
                if node[1] in ["Hookshot", "Grey Key", "Gold Key", "Bridge"]:
                    color_map.append("lightgreen")
                else:
                    color_map.append("yellow")
            net.draw(g, with_labels=True, node_color=color_map)
            plt.savefig(filename(), format="PNG")
            plt.clf()
            g.clear()
        return g


class Exits_debug(Exits):
    def nodes(self, save:bool=False,*,simplified=False, planar=False, spectral=False, spring=False):
        def filename():
            string = f"Graph-{self.world_i}_Exits"
            if simplified:
                string += "_simplified"
            return string + ".png"
        if simplified:
            g = self.nodes_simplified()
        else:
            g = super().nodes()
        if save:
            if planar:
                net.draw_planar(g, with_labels=True, node_color='yellow')
            elif spectral:
                net.draw_spectral(g, with_labels=True, node_color='yellow')
            elif spring:
                net.draw_spring(g, with_labels=True, node_color='yellow')
            else:
                net.draw(g, with_labels=True, node_color='yellow')
            plt.savefig(filename(), format="PNG")
            plt.clf()
            g.clear()
        return g

    def nodes_simplified(self):
        g = net.DiGraph()
        for B7, screen in enumerate(self.screens_ids):
            for sortie in self[screen]:
                net.add_path(g, [B7, sortie.destination])
        return g



def randomize(worlds, preprint=False, postprint=False):
    with open("Vanilla.smc", "rb") as game:
        test = debug(game.read())
        for x in worlds:
            testing = test.Worlds[x]
            if preprint: print(testing)
            testing.nodes(save=True)
            if postprint: print(testing)
        test.save()


if __name__ == "__main__":
    for x in range(5):
        randomize([x])  # Randomize, then save.
