from exits import Exits
from gameclass import GT
from locks import Locks
from copy import deepcopy
import random
from generic import room_to_index
from world import World
import networkx as net # version 2.5
import matplotlib.pyplot as plt
from items import Items

class debug(GT):
    def __init__(self, data):
        def world_indexes(world:int):
            """Returns the screen indexes of the provided world"""
            assert 0 <= world <= 4, "World must be 0, 1, 2, 3 or 4"
            id_per_world =   [0, 16, 32, 58, 88, 114]
            return range(id_per_world[world], id_per_world[world+1])

        super().__init__(data)
        del self.Worlds
        self.Worlds = [World_debug(self.data, x, world_indexes(x)) for x in range(5)]

    def save(self):
        super().save("debug.smc")


class World_debug(World):
    def __init__(self, data, world_i, screens_ids):
        self.world_i = world_i
        self.data = data
        self.screens = screens_ids

        self.Exits = Exits_debug(self.data,self.world_i, self.screens)
        self.Items = Items_debug(self.data, self.world_i, self.screens)
        self.Doors = Locks_debug(self.data, self.world_i, self.screens, self.Exits, self.Items)

    def __call__(self):
        super().__call__()
        self.Doors = Locks_debug(self.data, self.world_i, self.screens, self.Exits, self.Items)

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

    def save_nodes(self, screens=None):
        g = self.nodes()
        color_map = []
        label_map = {}
        
        if screens:
            for node in deepcopy(g.nodes):
                if node[:2] == "OO": 
                    g.remove_node(node)
                elif isinstance(node, str) and int(node[:2]) not in screens:
                    g.remove_node(node)
            g.remove_nodes_from(list(net.isolates(g)))
        
        for node in deepcopy(g.nodes):
            if isinstance(node, tuple) and node[1] in ["Red Gem", "Cherry", "Blue Gem"]:
                g.remove_node(node)


        for node in g:
            if node[1] in ["Hookshot", "Grey Key", "Gold Key", "Bridge"]:
                color_map.append("lightgreen")
            else:
                color_map.append("yellow")
            if isinstance(node, tuple):
                label_map[node] = node[1]
            else:
                label_map[node] = node
        net.draw(g, with_labels=True,labels=label_map, node_color=color_map)
        plt.savefig(f'graph/World {self.world_i}.png', format="PNG")
        plt.clf()


class Locks_debug(Locks):
    def save_nodes(self):
        g = super().nodes()
        color_map = []
        label_map = {}
        for node in g:
            if node[1] in ["Hookshot", "Gray Key", "Gold Key", "Bridge"]:
                color_map.append("lightgreen")
            else:
                color_map.append("yellow")
            if isinstance(node, tuple):
                label_map[node] = node[1]
            else:
                label_map[node] = node

        net.draw(g, pos=net.planar_layout(g),labels=label_map, with_labels=True, node_color=color_map)
        plt.savefig(f'graph/Locks {self.world_i}.png', format="PNG")
        plt.clf()
        print(f"Locks {self.world_i} nodes saved!")


class Items_debug(Items):
    def save_nodes(self,exits):
        g = super().nodes(exits)

        for node in deepcopy(g.nodes):
            if isinstance(node, tuple):
                if node[1] not in ["Hookshot", "Gray Key", "Gold Key", "Bridge"]:
                    g.remove_node(node)

        g.remove_nodes_from(list(net.isolates(g)))


        color_map = []
        label_map = {}
        for node in g:
            # Color map
            if node[1] in ["Hookshot", "Gray Key", "Gold Key", "Bridge"]:
                color_map.append("lightgreen")
            else:
                color_map.append("yellow")

            if isinstance(node, tuple):
                label_map[node] = node[1]
            else:
                label_map[node] = node

        net.draw(g, pos=net.circular_layout(g), with_labels=True, node_color=color_map, labels=label_map)
        plt.savefig(f'graph/Items {self.world_i}.png', format="PNG")
        plt.clf()
        print(f"Items {self.world_i} nodes saved!")
        return g


class Exits_debug(Exits):
    def save_nodes(self, screens=None):
        g = super().nodes()
        if screens:
            for node in deepcopy(g.nodes):
                if int(node[:2]) not in screens:
                    g.remove_node(node)
        net.draw(g,pos=net.spring_layout(g), with_labels=True, node_color='yellow')
        plt.savefig(f"graph/Exits {self.world_i}.png", format="PNG")
        plt.clf()
        print(f"Exits {self.world_i} nodes saved!")
        return g

    def save_nodes_simplified(self):
        def filename():
            string = f"graph/exits/Graph-{self.world_i}_simplified"
            return string + ".png"

        g = net.DiGraph()
        for B7, screen in enumerate(self.screens_ids):
            for sortie in self[screen]:
                net.add_path(g, [B7, sortie.destination])
        net.draw(g,pos=net.spring_layout(g), with_labels=True, node_color='yellow')
        plt.savefig(filename(), format="PNG")
        plt.clf()
        return g


    def adjacent_screens(self,*B7s):
        toreturn = set()
        for B7 in B7s:
            toadd = {B7}
            for sortie in self[room_to_index(tup=(self.world_i, B7))]:
                toadd.add(sortie.destination)
            toreturn = toreturn.union(toadd)
        print(toreturn)
        return toreturn

if __name__ == "__main__":
    # raise BaseException(room_to_index(tup=(4,2)))
    random.seed(0)
    world_id = 1
    # Banana - Red Diamond - Cherry - Banana - Cherry
    with open("Vanilla.smc", "rb") as game:
        test = debug(game.read())
        testing = test.Worlds[world_id]
        testing()
