from generic import room_to_index
from copy import deepcopy
import networkx as net # version 2.5

class Doors():
    def __init__(self, data, world_i,screens):
        # For now, it's fixed. So no calculs or calling to do.
        self.data = data
        self.world_i = world_i
        self.screens = screens

    def nodes(self, exits, items):
        g = net.DiGraph()
        items_names = {0x8 : "Hookshot", 0xA : "Gray Key",0xB : "Gold Key", 0xE : "Bridge"}

        all_locks = {
                    5: {"Gray Key": [("5 (N)","8 (S)"), ("8 (S)", "5 (N)")]},
                    8: {"Gray Key": [("8 (S)","5 (N)"), ("5 (N)","8 (S)") ]},
                    7: {"Bridge" :[("7 (N)", "7 (S)"), ("7 (S)", "7 (N)")]},
                    
                    23: {"Hookshot" : [("7 (S)", "7 (C)"), ("7 (C)", "7 (S)")],
                            "Bridge" : [("7 (C)", (7, items_names[items[23,0]], 0)), ("7 (C)", (7, items_names[items[23,1]], 1))]},
                    24: {   "Hookshot": [("8 (N)", (8, items_names[items[24,0]] , 0)), ("8 (N)", (8, items_names[items[24,1]] , 1))],
                            "Gray Key": [("8 (N)", exits.find("8 (N)"))]}, # W1 door just before the worst puzzle
                    26: {"Gray Key": [("10 (N)", "12 (S)")]}, # W1 door on the water screen.
                    28: {"Gray Key": [("12 (S)", "10 (N)")]}, # W1 door on screen north of the water screen.


                    35: {"Gray Key": [("3 (N)",  exits.find("3 (N)")),]},  # W2 : Screen with holes
                    42: {"Bridge": [("10 (E)", "10 (C)"),("10 (C)", "10 (E)"), ("10 (N)",(10, items_names[items[42,0]] , 0))]},
                    44: {"Gray Key": [("12 (S)", exits.find("12 (S)")),]}, # W2 : Screeen with some pyramids and enemies
                    45: {"Gray Key": [("13 (W)",  exits.find("13 (W)")),]},  # W2 : Boulder screen
                    49: {   "Hookshot": [("17 (N)", (17, items_names[items[49,0]] , 0))],
                            "Gray Key": [("17 (N)","17 (↗)"),]},  # W2 : Center Gray lock door
                    51: {"Gray Key": [("19 (S)", exits.find("19 (S)")),]},  # W2 : Screen just before the center gray
                    53: {   "Hookshot": [("21 (W)", "21 (↗)"), ("21 (↗)", "21 (W)")],
                            "Gray Key": [("21 (W)",  exits.find("21 (W)"),),]},  # W2 : moving platform!

                    80: {"Hookshot": [("22 (N)", "24 (S)"), ("24 (S)", "22 (N)")]},  # Waterfall

                    100:{   "Hookshot" : [("12 (N)", "12 (S)"), ("12 (S)", "12 (N)")],
                            "Gray Key": [("12 (N)", exits.find("12 (N)")),]}  # W4 : Firebreather screen
                                    }
        self.world_locks = {}
        for screen in all_locks:
            if screen in self.screens:
                self.world_locks[screen] = all_locks[screen]
                for list_nodes in all_locks[screen].values():
                    for node1, node2 in list_nodes:
                        g.add_edge(node1, node2)
        return g

