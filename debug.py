from gameclass import GT
from infos import *  # This is for the tools in infos.
from datetime import datetime
from world import *

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import cv2
import numpy as np

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

    def showMap(self, world_i, show_exits=True, show_items=True):
        this_world = self.all_worlds[world_i]
        
        #map
        filenames = ['map0.png','map1.png','map2.png','map3.png','map4.png']
        img = cv2.imread('maps/'+filenames[this_world.world_i])
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        fig,ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(RGB_img)

        # frames and items
        frame_size = (256, 221)
        all_worlds_frame_positions = [[(128, 1442),(384, 1442),(384, 1221),(384, 1000),(640, 1000),(128, 779),(384, 779),(640, 779),(128, 558),(384, 558),(640, 558),(640, 337),(128, 337),(384, 337),(128, 116),(128, 1221)],
                                        [(384, 2110),(384, 1889),(384, 1668),(384, 1447),(128, 1447),(128, 1226),(128, 1005),(384, 1226),(384, 1005),(384, 784),(640, 784),(896, 784),(640, 563),(896, 563),(896, 342),(896, 121)],
                                        [(1195, 1292),(1195, 1071),(939, 1071),(1451, 1071),(939, 850),(1195, 850),(1451, 850),(939, 629),(1195, 629),(1451, 629),(384, 1255),(640, 1255),(128, 1034),(384, 1034),(640, 1034),(128, 1255),(281, 746),(537, 746),(281, 525),(537, 525),(837, 333),(1093, 333),(837, 112),(1093, 112),(1464, 333),(1464, 112)],
                                        [(384, 3580),(128, 3580),(384, 3359),(384, 3138),(640, 3138),(896, 3138),(896, 2917),(640, 2917),(896, 2696),(896, 2254),(1152, 2254),(1408, 2254),(896, 2033),(1408, 2033),(640, 2033),(1408, 1591),(640, 1591),(1152, 1591),(896, 1370),(1152, 1370),(1152, 1149),(1152, 928),(1152, 707),(1408, 707),(1152, 486),(1152, 265),(896, 2475),(640, 1370),(640, 1812),(1408, 1812)],
                                        [(128, 1350),(128, 1129),(384, 1129),(1003, 1334),(747, 1334),(747, 1113),(1003, 1113),(1259, 1113),(1259, 1334),(2065, 1334),(1809, 1334),(1809, 1113),(1553, 1113),(1553, 1334),(2065, 1113),(1809, 892),(2065, 892),(1553, 892),(747, 892),(1003, 892),(1259, 892),(2065, 141),(2065, 362),(2065, 583),(1809, 362),(1809, 141)]]
        frame_positions = all_worlds_frame_positions[this_world.world_i]
        for frame_i in range(this_world.nFrames):
            base_pos = frame_positions[frame_i]
            ax.add_patch(Circle((base_pos[0],base_pos[1]),24, color='w'))
            ax.text(base_pos[0],base_pos[1],str(frame_i),fontsize=11,
                    horizontalalignment='center', verticalalignment='center')

            if show_items:#items
                if frame_i in this_world.items.frames: 
                    item_i = [i for i, x in enumerate(this_world.items.frames) if x == frame_i] #items in this frame
                    item_name = [this_world.items.names[i] for i in item_i]
                    ax.text(base_pos[0],base_pos[1]+40,str(item_i),fontsize=7,
                        horizontalalignment='center', verticalalignment='center', color='w')
                    ax.text(base_pos[0],base_pos[1]+65,str(item_name),fontsize=5,
                        horizontalalignment='center', verticalalignment='center', color='w')

        
        #exits
        if show_exits:
            for i,source in enumerate(this_world.exits.source_frames):
                this_color = list(1-np.random.choice(range(256), size=3)/300)
                #source exit
                base_pos = frame_positions[source]
                source_pos = (base_pos[0]-frame_size[0]/2+this_world.exits.source_Xpos[i], base_pos[1]-frame_size[1]/2+this_world.exits.source_Ypos[i])
                ax.add_patch(Circle(source_pos,5, color=this_color))
                ax.text(source_pos[0],source_pos[1],str(i),fontsize=10,
                        horizontalalignment='center', verticalalignment='center', color='red')
                #target exit
                base_pos = frame_positions[this_world.exits.destination_frames[i]]
                target_pos = (base_pos[0]-frame_size[0]/2+this_world.exits.destination_Xpos[i], base_pos[1]-frame_size[1]/2+this_world.exits.destination_Ypos[i])
                ax.arrow(source_pos[0],source_pos[1],target_pos[0]-source_pos[0], target_pos[1]-source_pos[1], 
                        head_width=15,length_includes_head=True, color=this_color)

        plt.show()
        return ''

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
    with open("GT__9439417113047506.smc", "rb") as original:
#    with open("Vanilla.smc", "rb") as original:
        startTime = datetime.now()
        game = randomized(original.read())
        game.showMap(0)

        # feasibility_results = []
        # early_boss_results = []
        # for m in range(200):
        #     unlocked_exits, unlocked_items, boss_reached, early_boss_indicator = game.all_worlds[2].feasibleWorldVerification()
        #     feasibility_results.append((all(unlocked_exits) and all(unlocked_items) and boss_reached))
        #     early_boss_results.append(early_boss_indicator)


        # print((sum(feasibility_results)/len(feasibility_results)))
        # print((sum(early_boss_results)/len(early_boss_results)))
        # #game.show_map(2)

        with open("debug.smc", "wb") as newgame:
            # print("Time taken to edit files : ", datetime.now() - startTime)
            print(f"Testing case have been created! {datetime.now()}")
            newgame.write(game.data)
