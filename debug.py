from gameclass import GT, ROM
import datetime
import random
from infos import *  # This is for the tools in infos.
from items import getter_items
from getters import *
from world import Exit

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

    def modify_exit(self, world_i, source_old_exit, destination_old_exit, source_new_exit, destination_new_exit):
        all_nFrames = [16, 16, 26, 30, 26]
        nFrames = all_nFrames[world_i]
        exits_offsets, exits_values, source_frames = getter_exits(self.data, world_i, nFrames)
        destination_frames = []
        for this_exit_values in exits_values:
            destination_frames.append(this_exit_values[0])
        for i in range(len(source_frames)): 
            if (source_frames[i]==source_old_exit)&(destination_frames[i]==destination_old_exit): #only when i is exit to modify
                for j in range(len(source_frames)): 
                    if (source_frames[j]==source_new_exit)&(destination_frames[j]==destination_new_exit): #only when j is new exit to reach
                        self[exits_offsets[i][0]] = exits_values[j][0]
                        self[exits_offsets[i][4]] = exits_values[j][4]
                        self[exits_offsets[i][5]] = exits_values[j][5]
        

info = infos()

with open("Vanilla.smc", "rb") as original:
    # random.seed("Value")
    game = debug(original.read())

    data = getter_exits(game.data, 1,0)[0]
    test2 = Exit(data)


    # Voici des exemples d'utilisation pour faire les 6 assignations nécessaires.
    a, b, c, d, e, f = test2.Tuple()
    print(a,b,c,d,e,f)

    # Voici à quoi pourrait ressembler l'assignation. Encore, proof of concept.
    # Évidement ça écrit aux mauvais endroits!
    for i, x in enumerate(range(10,17)):
        game.data[x] = test2.Tuple()[i]
        print(game.data[x])


    with open("debug.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)
