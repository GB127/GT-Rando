from gameclass import GT, ROM
import datetime
import random
from infos import *  # This is for the tools in infos.
from items import getter_items
from getters import getter_passwords

class debug(GT):
    def set_dark_room(self, world, room):
        self[0x186B5] = world
        self[0x186B6] = room

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

        Cherry = 0x0
        Banana = 0x1

        self.setmulti(0x1C67F, 0x1C692, 0x0)
        self[0x1c680] = 0x1
        self[0x1c686] = 0x1
        self[0x1c68c] = 0x1
        self[0x1c692] = 0x1


info = infos()

with open("Vanilla.smc", "rb") as original:
    # random.seed("Value")
    game = debug(original.read())

    with open("debug.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)
