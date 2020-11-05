import random
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle
import cv2
import numpy as np
from exits import *
from items import *

class World():
    def __init__(self, data, world_i):
        assert isinstance(data, bytearray), "Must be a bytearray"
        assert 0 <= world_i <= 4, "Must be in range 0-4."

        all_nFrames = [16, 16, 26, 30, 26]
        self.world_i = world_i
        self.data = data
        self.nFrames = all_nFrames[world_i]
        self.exits = Exits(data, world_i)
        self.original_exits = deepcopy(self.exits)
        #self.items = Items(data, world_i)

    def randomizeExits(self, fix_boss_exit, fix_locked_doors, keep_direction, pair_exits):
        self.exits.randomize(fix_boss_exit, fix_locked_doors, keep_direction, pair_exits)

    def setExit(self, source_exit, destination_exit):
        self.exits.setExit(source_exit, destination_exit)

    def randomizeItems(self):
        self.items.randomize()

    def showMap(self):
        
        #map
        filenames = ['map0.png','map1.png','map2.png','map3.png','map4.png']
        img = cv2.imread('maps/'+filenames[self.world_i])
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        fig,ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(RGB_img)

        # centers
        step_size = (256, 221)
        all_worlds_frame_positions = [[(128, 1442),(384, 1442),(384, 1221),(384, 1000),(640, 1000),(128, 779),(384, 779),(640, 779),(128, 558),(384, 558),(640, 558),(640, 337),(128, 337),(384, 337),(128, 116),(128, 1221)],
                                        [(384, 2110),(384, 1889),(384, 1668),(384, 1447),(128, 1447),(128, 1226),(128, 1005),(384, 1226),(384, 1005),(384, 784),(640, 784),(896, 784),(640, 563),(896, 563),(896, 342),(896, 121)],
                                        [(1195, 1292),(1195, 1071),(939, 1071),(1451, 1071),(939, 850),(1195, 850),(1451, 850),(939, 629),(1195, 629),(1451, 629),(384, 1255),(640, 1255),(128, 1034),(384, 1034),(640, 1034),(128, 1255),(281, 746),(537, 746),(281, 525),(537, 525),(837, 333),(1093, 333),(837, 112),(1093, 112),(1464, 333),(1464, 112)],
                                        [(384, 3580),(128, 3580),(384, 3359),(384, 3138),(640, 3138),(896, 3138),(896, 2917),(640, 2917),(896, 2696),(896, 2254),(1152, 2254),(1408, 2254),(896, 2033),(1408, 2033),(640, 2033),(1408, 1591),(640, 1591),(1152, 1591),(896, 1370),(1152, 1370),(1152, 1149),(1152, 928),(1152, 707),(1408, 707),(1152, 486),(1152, 265),(896, 2475),(640, 1370),(640, 1812),(1408, 1812)],
                                        [(128, 1350),(128, 1129),(384, 1129),(1003, 1334),(747, 1334),(747, 1113),(1003, 1113),(1259, 1113),(1259, 1334),(2065, 1334),(1809, 1334),(1809, 1113),(1553, 1113),(1553, 1334),(2065, 1113),(1809, 892),(2065, 892),(1553, 892),(747, 892),(1003, 892),(1259, 892),(2065, 141),(2065, 362),(2065, 583),(1809, 362),(1809, 141)]]
        frame_positions = all_worlds_frame_positions[self.world_i]
        for i in range(self.nFrames):
            base_pos = frame_positions[i]
            ax.add_patch(Circle(base_pos,22, color='w'))
            ax.text(base_pos[0],base_pos[1],str(i),fontsize=10,
                    horizontalalignment='center', verticalalignment='center')
        
        #exits
        for i,source in enumerate(self.exits.source_frames):
            this_color = list(1-np.random.choice(range(256), size=3)/300)
            #source exit
            base_pos = frame_positions[source]
            source_pos = (base_pos[0]-step_size[0]/2+self.exits.source_Xpos[i], base_pos[1]-step_size[1]/2+self.exits.source_Ypos[i])
            ax.add_patch(Circle(source_pos,5, color=this_color))
            ax.text(source_pos[0],source_pos[1],str(i),fontsize=10,
                    horizontalalignment='center', verticalalignment='center', color='r')
            #target exit
            base_pos = frame_positions[self.exits.destination_frames[i]]
            target_pos = (base_pos[0]-step_size[0]/2+self.exits.destination_Xpos[i], base_pos[1]-step_size[1]/2+self.exits.destination_Ypos[i])
            ax.arrow(source_pos[0],source_pos[1],target_pos[0]-source_pos[0], target_pos[1]-source_pos[1], 
                    head_width=15,length_includes_head=True, color=this_color)

        plt.show()
        return ''

