import random
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from matplotlib.patches import Circle
import numpy as np
from exits import *

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

    def randomizeExits(self, fix_boss_exit, keep_direction, pair_exits):
        self.exits.randomize(fix_boss_exit, keep_direction, pair_exits)

    def showMap(self):
        
        #map
        filenames = ['map0.png','map1.png','map2.png','map3.png','map4.png']
        img = cv2.imread(filenames[self.world_i])
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        fig,ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(RGB_img)

        # centers
        step_size = (256, 221)
        origins = [(128,1442),(128,1300),(128, 1255),(128, 3580)]
        origin = origins[self.world_i]
        all_worlds_frame_positions = [[(0,0),(1,0),(1,1),(1,2),(2,2),(0,3),(1,3),(2,3),(0,4),(1,4),(2,4),(2,5),(0,5),(1,5),(0,6),(0,1)],
                                    [(1,0),(1,1),(1,2),(1,3),(0,3),(0,4),(0,5),(1,4),(1,5),(1,6),(2,6),(3,6),(2,7),(3,7),(3,8),(3,9)],
                                    [(4.17,-0.17),(4.17,0.83),(3.17,0.83),(5.17,0.83),(3.17,1.83),(4.17,1.83),(5.17,1.83),(3.17,2.83),(4.17,2.83),(5.17,2.83),   (1,0),(2,0),(0,1),(1,1),(2,1),(0,0),   (0.6,2.3),(1.6,2.3),(0.6,3.3),(1.6,3.3),   (2.77,4.17),(3.77,4.17),(2.77,5.17),(3.77,5.17),  (5.22,4.17),(5.22,5.17)],
                                    [(1,0),(0,0),(1,1),(1,2),(2,2),(3,2),(3,3),(2,3),(3,4),(3,6),(4,6),(5,6),(3,7),(5,7),(2,7),(5,9),(2,9),(4,9),(3,10),(4,10),(4,11),(4,12),(4,13),(5,13),(4,14),(4,15),  (3,5),(2,10),(2,8),(5,8)],
                                    []]
        frame_positions = all_worlds_frame_positions[self.world_i]
        for frame in range(self.nFrames):
            this_pos = (origin[0]+frame_positions[frame][0]*step_size[0], 
                        origin[1]-frame_positions[frame][1]*step_size[1])
            ax.add_patch(Circle(this_pos,22, color='w'))
            ax.text(this_pos[0],this_pos[1],str(frame),fontsize=10,
                    horizontalalignment='center', verticalalignment='center')
        
        #exits
        for i,source in enumerate(self.exits.source_frames):
            this_color = list(1-np.random.choice(range(256), size=3)/300)
            #source exit
            this_pos = (origin[0]+frame_positions[source][0]*step_size[0], 
                        origin[1]-frame_positions[source][1]*step_size[1])
            if self.exits.source_types[i] == 'N':
                source_pos = (this_pos[0],this_pos[1]-step_size[1]*0.4)
            elif self.exits.source_types[i] == 'S':
                source_pos = (this_pos[0],this_pos[1]+step_size[1]*0.4)
            elif self.exits.source_types[i] == 'W':
                source_pos = (this_pos[0]-step_size[0]*0.4, this_pos[1])
            elif self.exits.source_types[i] == 'E':
                source_pos = (this_pos[0]+step_size[0]*0.4, this_pos[1])
            elif self.exits.source_types[i] == '?':
                source_pos = (this_pos[0]+step_size[0]*0.2, this_pos[1]+step_size[1]*0.2)
            
            ax.add_patch(Circle(source_pos,5, color=this_color))
            #target exit
            this_pos = (origin[0]+frame_positions[self.exits.destination_frames[i]][0]*step_size[0], 
                        origin[1]-frame_positions[self.exits.destination_frames[i]][1]*step_size[1])
            if self.exits.destination_types[i] == 'N':
                target_pos = (this_pos[0],this_pos[1]-step_size[1]*0.4)
            elif self.exits.destination_types[i] == 'S':
                target_pos = (this_pos[0],this_pos[1]+step_size[1]*0.4)
            elif self.exits.destination_types[i] == 'W':
                target_pos = (this_pos[0]-step_size[0]*0.4, this_pos[1])
            elif self.exits.destination_types[i] == 'E':
                target_pos = (this_pos[0]+step_size[0]*0.4, this_pos[1])
            elif self.exits.destination_types[i] == '?':
                target_pos = (this_pos[0]+step_size[0]*0.2, this_pos[1]+step_size[1]*0.2)
            ax.arrow(source_pos[0],source_pos[1],target_pos[0]-source_pos[0], target_pos[1]-source_pos[1], 
                    head_width=15,length_includes_head=True, color=this_color)

        plt.show()
        return ''

