from gameclass import GT
from infos import *  # This is for the tools in infos.
from datetime import datetime
from world import *

class debug(GT):
    def __str__(self):
        string = ""
        for world in self.all_worlds:
            string += str(world)
        return string


    def print_world(self, world_i, arg=None):
        if arg == "items": 
            print(f"World {world_i} items")
            print(self.all_worlds[world_i].items)
        else: print(self.all_worlds[world_i])


    def __init__(self,data):
        self.list_freespace()
        super().__init__(data, seed="Debug")



    def list_freespace(self):
        self.freespace = [offset for offset in range(0x7374, 0x7FB0)]
        self.freespace += [offset for offset in range(0xFF33, 0x10000)]
        self.freespace += [offset for offset in range(0x1401, 0x15E00)]
        self.freespace += [offset for offset in range(0x1F9C1, 0x1FA42)]
        self.freespace += [offset for offset in range(0x1FADC, 0x20000)]
        self.freespace += [offset for offset in range(0x2A796, 0x2C000)]
        self.freespace += [offset for offset in range(0x47DFE, 0x48000)]
        self.freespace += [offset for offset in range(0x45055, 0x4F100)]
        self.freespace += [offset for offset in range(0x4FD48, 0x50000)]
        self.freespace += [offset for offset in range(0x53F70, 0x54000)]
        self.freespace += [offset for offset in range(0x55FC0, 0x56000)]
        self.freespace += [offset for offset in range(0x57E00, 0x58000)]
        self.freespace += [offset for offset in range(0x5E240, 0x5F000)]
        self.freespace += [offset for offset in range(0x5FBDC, 0x5FE00)]
        self.freespace += [offset for offset in range(0xFB5BE, 0xFD400)]
        self.freespace += [offset for offset in range(0x7FB20, 0x7FE00)]
        self.freespace += [offset for offset in range(0x7FE50, 0x7FEA0)]
        self.freespace += [offset for offset in range(0x7FED0, 0x7FF00)]
        self.freespace += [offset for offset in range(0x7FFB0, 0x7FFFF)]

        self.used = []

    def quick_bosses(self):
        #self[0xB4AB] = 0x1  # For now, only kill one to clear the boss for world 0.

        self[0xC563] = 0x1

    def early_bosses(self):
        """Changes exits so that bosses are reached within the very first exit of a world!
        """
        self[0x1F3ED] = 14
        self[0x1F4C3] = 15
        self[0x1F58D] = 25
        self[0x1f6f7] = 25
        self[0x1f6f7 + 4] = 180
        self[0x1F877] = 25

    def show_map(self, world_i):
        self.all_worlds[world_i].showMap()

    def setExit(self, world_i, source_exit, destination_exit, match=False):
        """Set a specific exit to a specific exit."""
        this_world = self.all_worlds[world_i]
        this_world.exits.setExit(source_exit, destination_exit)
        self[this_world.exits.offsets[source_exit][0]] = this_world.exits.destination_frames[source_exit]
        self[this_world.exits.offsets[source_exit][4]] = this_world.exits.destination_Xpos[source_exit]
        self[this_world.exits.offsets[source_exit][5]] = this_world.exits.destination_Ypos[source_exit]
        #hook bug fix
        if self[this_world.exits.offsets[source_exit][3]]>=2**7:self[this_world.exits.offsets[source_exit][3]] = self[this_world.exits.offsets[source_exit][3]]-2**7
        self[this_world.exits.offsets[source_exit][3]] = self[this_world.exits.offsets[source_exit][3]]+this_world.exits.destination_hookshotHeightAtArrival[source_exit]*2**7

        if match:
            self.setExit(world_i, destination_exit, source_exit)

    def disable_heart_loss(self):
        self[0x5D1B] = 0xEA
        self[0x5D1C] = 0xEA

    def speed_goofy(self, value):
        self[0x18E1B] -= value
        self[0x18E1D] += value

        self[0x18E2B] += value
        self[0x18E2D] -= value

        self[0x18E17] -= value
        self[0x18E27] += value


        self[0x18E23] += value
        self[0x18E33] -= value




    def __setitem__(self,offset, value):
        if offset in self.freespace:
            self.used.append(offset)
            self.freespace.pop(self.freespace.index(offset))
        super().__setitem__(offset,value)

    def set_item(self, world_i,item_i,  value):
        self.all_worlds[world_i].items.set_item(item_i, value)
        self.all_worlds[world_i].writeWorldInData()

    def do_not_place_keydoors(self):
        self[0x14377] = 0xEA
        self[0x14378] = 0xEA

info = infos()

def set_seed(seed=None):
    if seed is None: test = str(random.random())[3:6]  # Au hasard. Restreint le nombre de chiffres
    print(seed)
    random.seed(seed)

class randomized(debug):
    def __init__(self, data):
        self.data = bytearray(data)
        self.all_worlds = [World(self.data, 0),World(self.data, 1),World(self.data, 2),World(self.data, 3),World(self.data, 4)]


if __name__ == "__main__":
    with open("GT_wdei_5323491536917113.smc", "rb") as original:
#    with open("Vanilla.smc", "rb") as original:
        startTime = datetime.now()
        game = randomized(original.read())


        feasibility_results = []
        early_boss_results = []
        for m in range(200):
            unlocked_exits, unlocked_items, boss_reached, early_boss_indicator = game.all_worlds[2].feasibleWorldVerification()
            feasibility_results.append((all(unlocked_exits) and all(unlocked_items) and boss_reached))
            early_boss_results.append(early_boss_indicator)


        print((sum(feasibility_results)/len(feasibility_results)))
        print((sum(early_boss_results)/len(early_boss_results)))
        #game.show_map(2)

        with open("debug.smc", "wb") as newgame:
            # print("Time taken to edit files : ", datetime.now() - startTime)
            print(f"Testing case have been created! {datetime.now()}")
            newgame.write(game.data)
