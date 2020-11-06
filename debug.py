from gameclass import GT, ROM
import datetime
import random
from infos import *  # This is for the tools in infos.
from items import getter_items
from getters import *
from exits import *
from world import *

class debug(GT):
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


    def show_map(self, world):
        self.all_worlds[world].showMap()


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


    def get_first_rooms(self):
        return [(0, self[0x1FFA7]),
                (1, self[0x1FFA8]),
                (2, self[0x1FFA9]),
                (3, self[0x1FFAA]),
                (4, self[0x1FFAB])]

info = infos()


with open("Vanilla.smc", "rb") as original:
    # random.seed("Value")
    game = debug(original.read())
    game.world_select()

    print(game.get_first_rooms())
    game.firstframe_randomizer()
    print(game.get_first_rooms())

    with open("debug.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)
