import networkx as net # version 2.5

class Locks():
    def __init__(self, data, world_i,screens, exits, items):
        """Needs items and exits to link locks to the correct items or spawns. Since we can't randomize, the data is pulled from a fixed data."""
        self.data = data
        self.world_i = world_i
        self.screens = screens

        items_names = {0x8 : "Hookshot", 0x9 : "Candle  ", 0xA : "Gray Key",0xB : "Gold Key", 0xC :"Shovel", 0xD : "Bell", 0xE : "Bridge"}
        fruits_names = {0x40 : "Cherry  ", 0x42: "Banana  ", 0x44 : "Red Gem ", 0x46 : "Blue Gem"}

        all_locks = {  # [lock, links]
                        5: [    ["Gray Key", [("5 (N)","8 (S)"), ("8 (S)", "5 (N)")]]],                    
                        8:  [   ["Gray Key", [("8 (S)","5 (N)"), ("5 (N)","8 (S)") ]]],
                        7:  [   ["Bridge" ,[("7 (N)", "7 (S)"), ("7 (S)", "7 (N)")]]],
                        12: [   ["Gold Key", [("12 (N)", "14 (S)")]]
                        ],
                        23: [   ["Hookshot", [("7 (S)", "7 (C)"), ("7 (C)", "7 (S)")]],
                                ["Bridge", [("7 (C)", (7, items_names[items[23,0]], 0)), ("7 (C)", (7, items_names[items[23,1]], 1))]]
                            ],
                        24: [   ["Hookshot", [("8 (N)", (8, items_names[items[24,0]] , 0)), ("8 (N)", (8, items_names[items[24,1]] , 1))]],
                                ["Gray Key", [("8 (N)", exits.find("8 (N)"))]]
                            ], # W1 door just before the worst puzzle
                        26: [   ["Gray Key", [("10 (N)", "12 (S)")]]], # W1 door on the water screen.
                        28: [   ["Gray Key", [("12 (S)", "10 (N)")]]], # W1 door on screen north of the water screen.
                        29: [   ["Hookshot", [("13 (W)", "13 (C)"), ("13 (C)", "13 (W)")]],
                                ["Hookshot", [("13 (N)", "13 (C)"), ("13 (C)", "13 (N)")]],
                            ],  # W1 : Double Hookshot.
                        30: [   ["Gold Key", [("14 (N)", "15 (S)")]]
                            ],
                        35: [   ["Gray Key", [("3 (N)",  exits.find("3 (N)")),]]],  # W2 : Screen with holes
                        42: [   ["Bridge", [("10 (E)", "10 (C)"),("10 (C)", "10 (E)")]],
                                ["Bridge", [("10 (N)",(10, items_names[items[42,0]] , 0))]]],  # W2 : Double bridge screen
                        44: [   ["Gray Key", [("12 (S)", exits.find("12 (S)")),]]], # W2 : Screeen with some pyramids and enemies
                        45: [   ["Gray Key", [("13 (W)",  exits.find("13 (W)")),]]],  # W2 : Boulder screen
                        49: [   ["Hookshot", [("17 (N)", (17, items_names[items[49,0]] , 0))]],
                                ["Gray Key", [("17 (N)","17 (↗)"),]]
                            ],  # W2 : Center Gray lock door
                        51: [   ["Gray Key", [("19 (S)", exits.find("19 (S)")),]]],  # W2 : Screen just before the center gray
                        53: [   ["Hookshot", [("21 (W)", "21 (↗)"), ("21 (↗)", "21 (W)")]],
                                ["Gray Key", [("21 (W)",  exits.find("21 (W)"),),]]
                            ],  # W2 : moving platform!
                        56: [   ["Gold Key", [("24 (N)", "25 (S)")]]
                        ],
                        80: [   ["Hookshot", [("22 (N)", "24 (S)"), ("24 (S)", "22 (N)")]]],  # Waterfall

                        90: [   ["Hookshot", [("2 (W)", "2 (↗)"),("2 (↗)", "2 (W)")]]],  # 4-2 : Hookshot the big hole
                        97: [   ["Hookshot", [("9 (↗)", "9 (W)"), ("9 (W)", "9 (↗)") ]],
                                ["Hookshot", [("9 (N)", "9 (W)"), ("9 (W)", "9 (N)") ]]
                            ],  # W4 : Double hookshot screen that don't have canons
                        100:[   ["Hookshot", [("12 (S)", "12 (N)"), ("12 (N)", "12 (S)")]],
                                ["Gray Key", [("12 (N)", exits.find("12 (N)")),]]
                            ],  # W4 : Firebreather screen
                        108: [   ["Gold Key", [("20 (W)", "20 (↗)")]]
                        ],
                        109:[   ["Hookshot", [("21 (↗)", "21 (C)"), ("21 (C)", "21 (↗)")]],
                                ["Hookshot", [("21 (S)", "21 (C)"), ("21 (C)", "21 (S)")]]
                            ]
                    }
        self.world_locks = {}
        for screen in all_locks:
            if screen in self.screens:
                self.world_locks[screen] = all_locks[screen]

    def nodes(self):
        """Returns: Digraph containing all locks."""
        locks_graph = net.DiGraph()
        for screen_locks in self.world_locks.values():
            for lock in screen_locks:
                for node1, node2 in lock[1]:
                    locks_graph.add_edge(node1, node2)
        return locks_graph

