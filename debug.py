from gameclass import GT, ROM
import datetime
import random
from infos import *  # This is for the tools in infos.
from items import getter_items
from getters import *


class debug(GT):
    def set_dark_room(self, world, frame):
        self[0x186B5] = world
        self[0x186B6] = frame

    def quick_bosses(self):
        self[0xB4AB] = 0x1  # For now, only kill one to clear the boss for world 0.

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

    def world_select(self):
        # Put a banana on the box of the world you want to go. Example  
            # Banana on the 3rd box = World 2 (3rd world of the game)
        # Cherry for all the rest of the boxes
        self.setmulti(0x1C67F, 0x1C692, 0x0)
        self[0x1c680] = 0x1
        self[0x1c686] = 0x1
        self[0x1c68c] = 0x1
        self[0x1c692] = 0x1

    def set_exit(self, world2, start, end, viceversa=False):  # Eventually, add the selection of which
        offsets_to_change = getter_exits(self.data, world2, Frames=[start])[0][0]  # For now, hardcorded to first
        print(offsets_to_change)
        all_exits_values = getter_exits(self.data, world2, Frames=range(10))[1]  # Je vais supposer qu'ici ça va chercher tous les rooms du world.
        for one_exit in all_exits_values:
            if one_exit[0] == end:
                for no, value in enumerate(one_exit):
                    self[offsets_to_change[no]] = value
                break
        if viceversa:
            self.set_exit(world2, end, start)



info = infos()

with open("Vanilla.smc", "rb") as original:
    # random.seed("Value")
    game = debug(original.read())
    game.exits_randomizer(1,1,1)
    """
    data = getter_exits(game.data, 1,Frames=[0])
    print(data)
    test2 = Exit(data[0])

    data2 = getter_exits(game.data, 1,Frames=range(25))  # Maintenant le range est ici.
    print(data2)


    data = getter_exits(game.data, 1,Frames=[0,4,6,2])
    print(data)
    test2 = Exit(data[0])



    data = getter_exits(game.data, 1,Frames=0)  # Lance une erreur
    """





    with open("debug.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)
