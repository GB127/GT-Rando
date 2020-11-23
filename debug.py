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


    def print_passwords(self, world=None):
        # J'aime mieux ceci dans debug, vu que l'on va imprimer
        # Le password seulement pour déboguer.
        translation = {0x0 : "Cherry",
                       0x1 : "Banana",
                       0x2 : "Red Gem",
                       0x3 : "Blue Gem"}
        if world is None:
            for one in range(1,5):
                self.print_passwords(one)
        else:
            data = f"World {world} :"
            for box in getter_passwords(world):
                data += f'{translation[self.data[box]]:^10}-'
            print(data.rstrip("-"))

    def print_darkframes(self):
        """Print the list of tuples that are dark rooms.
            """
        print(f'{len(self.get_darkrooms())} Dark rooms: {self.get_darkrooms()}')

    def print_iceframes(self):
        """Print the list of tuples that are ice rooms
            """
        print(f'{len(self.get_icerooms())} Ice rooms: {self.get_icerooms()}')

    def get_darkframes(self):
        """Generate a list of tuples that contains the different frames that are darks.

            Returns:
                list: list of tuples
                    tuples : (World, Frame)
                        World : int
                        Frame : int
            """
        toreturn = []
        for no, offset in enumerate(range(0x1FF35, 0x1FFA7)):
            if self[offset] & 2:
                if no in range(0, 16):
                    toreturn.append((0, no))
                elif no in range(16, 32):
                    toreturn.append((1, no - 16))
                elif no in range(32, 58):
                    toreturn.append((2, no - 32))
                elif no in range(58, 88):
                    toreturn.append((3, no - 58))
                else:
                    toreturn.append((4, no - 88))
        return toreturn

    def get_iceframes(self):
        """Generate a list of tuples that contains the different frames that are icy.

            Returns:
                list: list of tuples
                    tuples : (World, Frame)
                        World : int
                        Frame : int
            """

        toreturn = []
        for no, offset in enumerate(range(0x1FF35, 0x1FFA7)):
            if self[offset] & 1:
                if no in range(0, 16):
                    toreturn.append((0, no))
                elif no in range(16, 32):
                    toreturn.append((1, no - 16))
                elif no in range(32, 58):
                    toreturn.append((2, no - 32))
                elif no in range(58, 88):
                    toreturn.append((3, no - 58))
                else:
                    toreturn.append((4, no - 88))
        return toreturn

    def __setitem__(self,offset, value):
        if offset in self.freespace:
            self.used.append(offset)
            self.freespace.pop(self.freespace.index(offset))
        super().__setitem__(offset,value)


    def get_first_rooms(self):
        return [(0, self[0x1FFA7]),
                (1, self[0x1FFA8]),
                (2, self[0x1FFA9]),
                (3, self[0x1FFAA]),
                (4, self[0x1FFAB])]

    def testExitsFromData(self, world_i, vanilla_data):
        all_nFrames = [16, 16, 26, 30, 26]
        nFrames = all_nFrames[world_i]
        this_world = self.all_worlds[world_i]
        exits_offsets_old, exits_values_old, exits_frames_old = this_world.exits.getExitsFromData_old(vanilla_data, world_i, nFrames) 
        exits_offsets, exits_values, exits_frames = this_world.exits.getExitsFromData(self.data, world_i, nFrames)
        return (exits_values_old == exits_values) and (exits_frames_old == exits_frames)

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
        game.setExit(0,0,12)

        tester_all(game.data)  # Tempo function for testing. Could be tweaked to become your request.

        # This code remove the checker fo keyed door. Comment these if you want to open the doors manually.
        game[0x14377] = 0xEA
        game[0x14378] = 0xEA



        # Values to change for 0-5. See tester_all to see how I got these offsets in the output.
            # It's a big byte so you need to consider these two values as a whole value (IE 0xXXXX, not 0xXX and 0xXX)

        # Amuses-toi bien :)

        game[0x83177] = # Your value
        game[0x83178] = # Your value



        with open("debug.smc", "wb") as newgame:
            # print("Time taken to edit files : ", datetime.now() - startTime)
            # print(f"Testing case have been created! {datetime.now()}")
            newgame.write(game.data)
