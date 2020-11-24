from gameclass import GT, ROM
import datetime
import random
from infos import *  # This is for the tools in infos.
from getters import *
from exits import *
from world import *
from doors import *
from datetime import datetime
from copy import deepcopy








class debug(GT):

    def __init__(self,data):
        self.list_freespace()
        super().__init__(data)

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

    def show_map(self, world_i):
        self.all_worlds[world_i].showMap()

    def __setitem__(self,offset, value):
        if offset in self.freespace:
            self.used.append(offset)
            self.freespace.pop(self.freespace.index(offset))
        super().__setitem__(offset,value)

    def do_not_place_doors(self):
        # This code remove the checker fo keyed door. Comment these if you want to open the doors manually.
        game[0x14377] = 0xEA
        game[0x14378] = 0xEA

info = infos()

def set_seed(seed=None):
    if seed is None: test = str(random.random())[3:6]  # Au hasard. Restreint le nombre de chiffres
    print(seed)
    random.seed(seed)




if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as original:
        startTime = datetime.now()
        game = debug(original.read())
        game.world_select()

        

        # Values to change for 0-5. See tester_all to see how I got these offsets in the output.
            # It's a big byte so you need to consider these two values as a whole value (IE 0xXXXX, not 0xXX and 0xXX)
            # Avec les valeurs actuelles, tu pourras ouvrir l'arbre à la gauche de la porte.


        # Amuses-toi bien :)
        print(hex(game[0x144EA]), game[0x144E9])  # Here how the game understand the number behind these two offsets.
        game[0x144EA] = 0x0 # Your value
        game[0x144E9] = 0xA# Your value


        game.setExit(0,0,12)

        with open("debug.smc", "wb") as newgame:
            # print("Time taken to edit files : ", datetime.now() - startTime)
            # print(f"Testing case have been created! {datetime.now()}")
            newgame.write(game.data)
