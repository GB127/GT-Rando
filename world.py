import random
from copy import deepcopy
from getters import getter_exits
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# import cv2  J'ai du commenter cela pour coder mes affaires, car je ne sais pas comment faire pour le régler. J'ai essayé pip install cv2 et ça n'a rien donné.
from matplotlib.patches import Circle
import numpy as np

class World():
    def __init__(self, data, world_i):
        assert isinstance(data, bytearray), "Must be a bytearray"
        assert 0 <= world_i <= 4, "Must be in range 0-4."

        all_nFrames = [16, 16, 26, 30, 26]
        all_bossFrame = [14, 15, 25, 25, 25]
        self.world_i = world_i
        self.data = data
        self.nFrames = all_nFrames[world_i]
        self.bossFrame = all_bossFrame[world_i]
        # Si je comprends bien ici, il faudra faire le loop proposé ici pour tout rassembler.
        self.exits_offsets, self.exits_values, self.source_frames = getter_exits(data, world_i, self.nFrames)
        self.original_exits_values = deepcopy(self.exits_values)
        self.determine_current_destinations()
        self.original_destination_pos = deepcopy(self.destination_pos)
        self.original_source_pos = deepcopy(self.source_pos) #self.source_pos becomes a useless variable afterwards
        for i,this_exit_values in enumerate(self.exits_values):
                if this_exit_values[0] == self.bossFrame:
                    self.preboss_index = i
                    break
        self.determine_current_pairs()
        self.original_exit_pairs = self.exit_pairs
        self.nExits = len(self.source_frames)

    def determine_current_destinations(self):
        self.destination_frames = []
        self.destination_pos = []
        self.source_pos = []
        for this_exit_values in self.exits_values:
            self.destination_frames.append(this_exit_values[0])
            if this_exit_values[4]<25:
                self.destination_pos.append('W')
                self.source_pos.append('E')
            elif this_exit_values[4]>230:
                self.destination_pos.append('E')
                self.source_pos.append('W')
            elif this_exit_values[5]<40:
                self.destination_pos.append('N')
                self.source_pos.append('S')
            elif this_exit_values[5]>190:
                self.destination_pos.append('S')
                self.source_pos.append('N')
            else:
                self.destination_pos.append('?') #stairs
                self.source_pos.append('?')

    def determine_current_pairs(self):
        self.exit_pairs = []
        for i,source in enumerate(self.source_frames):
            for j,destination in enumerate(self.destination_frames):
                if (self.destination_frames[i] == self.source_frames[j])&(self.destination_frames[j] == self.source_frames[i]):
                    if sorted([i,j]) not in self.exit_pairs: 
                        self.exit_pairs.append(sorted([i,j]))

    def determine_new_order(self, fix_boss_exit, keep_direction, pair_exits):

        new_order = list(range(self.nExits))
        if keep_direction & (not pair_exits):#keep direction
            for ref_destination_pos in ['N','S','W','E','?']:
                i_to_shuffle_now = [i for i, this_destination_pos in enumerate(self.destination_pos) if this_destination_pos == ref_destination_pos]
                if fix_boss_exit: 
                    if self.preboss_index in i_to_shuffle_now: i_to_shuffle_now.remove(self.preboss_index)
                shuffled_i = deepcopy(i_to_shuffle_now)
                random.shuffle(shuffled_i)
                for j,i in enumerate(i_to_shuffle_now):
                    new_order[i] = shuffled_i[j]

        elif (not keep_direction) & (pair_exits):#pair exits
            shuffled_pairs = deepcopy(self.exit_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(self.exit_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]

        elif keep_direction & pair_exits: #keep direction AND pair exits
            pairs_to_sort = deepcopy(self.exit_pairs)
            NS_pairs = []
            WE_pairs = []
            stairs_pairs = []
            for pair in pairs_to_sort:
                if (self.destination_pos[pair[0]] == 'N') or (self.destination_pos[pair[0]] == 'S'):
                    NS_pairs.append(pair)
                elif (self.destination_pos[pair[0]] == 'W') or (self.destination_pos[pair[0]] == 'E'):
                    WE_pairs.append(pair)
                elif (self.destination_pos[pair[0]] == '?'):
                    stairs_pairs.append(pair)
            #North and South pairs
            shuffled_pairs = deepcopy(NS_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(NS_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]
            #West and East pairs
            shuffled_pairs = deepcopy(WE_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(WE_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]
            #stairs pairs
            shuffled_pairs = deepcopy(stairs_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(stairs_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]

        else: #totally random
            random.shuffle(new_order)
            if fix_boss_exit:
                new_order.remove(self.preboss_index)
                new_order.insert(self.preboss_index,self.preboss_index)

        return new_order

    def randomize_exits(self, fix_boss_exit, keep_direction, pair_exits): #fix_boss_exit is a bool
        
        #determine new order
        new_order = self.determine_new_order(fix_boss_exit, keep_direction, pair_exits)

        #assign elements in new order
        old_exits_values = deepcopy(self.original_exits_values)
        for i,temp in enumerate(old_exits_values):
            self.exits_values[i][0] = old_exits_values[new_order[i]][0]
            self.exits_values[i][4] = old_exits_values[new_order[i]][4]
            self.exits_values[i][5] = old_exits_values[new_order[i]][5]

        self.determine_current_destinations()

        return self.exits_values

    def show_map(self):
        
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
        for i,source in enumerate(self.source_frames):
            this_color = list(1-np.random.choice(range(256), size=3)/300)
            #source exit
            this_pos = (origin[0]+frame_positions[source][0]*step_size[0], 
                        origin[1]-frame_positions[source][1]*step_size[1])
            if self.original_source_pos[i] == 'N':
                source_pos = (this_pos[0],this_pos[1]-step_size[1]*0.4)
            elif self.original_source_pos[i] == 'S':
                source_pos = (this_pos[0],this_pos[1]+step_size[1]*0.4)
            elif self.original_source_pos[i] == 'W':
                source_pos = (this_pos[0]-step_size[0]*0.4, this_pos[1])
            elif self.original_source_pos[i] == 'E':
                source_pos = (this_pos[0]+step_size[0]*0.4, this_pos[1])
            elif self.original_source_pos[i] == '?':
                source_pos = (this_pos[0]+step_size[0]*0.2, this_pos[1]+step_size[1]*0.2)
            ax.add_patch(Circle(source_pos,5, color=this_color))
            #target exit
            this_pos = (origin[0]+frame_positions[self.destination_frames[i]][0]*step_size[0], 
                        origin[1]-frame_positions[self.destination_frames[i]][1]*step_size[1])
            if self.destination_pos[i] == 'N':
                target_pos = (this_pos[0],this_pos[1]-step_size[1]*0.4)
            elif self.destination_pos[i] == 'S':
                target_pos = (this_pos[0],this_pos[1]+step_size[1]*0.4)
            elif self.destination_pos[i] == 'W':
                target_pos = (this_pos[0]-step_size[0]*0.4, this_pos[1])
            elif self.destination_pos[i] == 'E':
                target_pos = (this_pos[0]+step_size[0]*0.4, this_pos[1])
            elif self.destination_pos[i] == '?':
                target_pos = (this_pos[0]+step_size[0]*0.2, this_pos[1]+step_size[1]*0.2)
            ax.arrow(source_pos[0],source_pos[1],target_pos[0]-source_pos[0], target_pos[1]-source_pos[1], 
                    head_width=15,length_includes_head=True, color=this_color)

        plt.show()
        return ''



class Exit:
    def __init__(self, list_values):
        """[summary]

            0 : Screen this exit leads to
            1 : Base tile index on collision map
            2 : Pas spécifié par psychomaniac
            3 : Type d'exit, It specifies how the exit's collision tiles are laid down, See below.
                If bit 6 is set (0x20) then it is a vertical line, otherwise it is horizontal or 2x2
                If bit 6 is not set and bits 1-4 are 0x0F, then the exit is 2x2 (x,y) (x+1,y) (x,y+1) and (x+1,y+1)
                For horizontal or vertical lines, bits 1-4 specify the length and bit 5 says if it is 1 or 2 tiles thick.
            4 : X position on the destination screen to place Max and/or Goofy
            5 : Y position on the destination screen to place Max and/or Goofy



        Args:
            list_values ([type]): [description]
        """
        self.destination = list_values[0]
        self.data1 = list_values[1]
        self.data2 = list_values[2]
        self.type = list_values[3]
        self.destinationx = list_values[4]
        self.destinationy = list_values[5]

    def Tuple(self):
        return self.destination, self.data1, self.data2, self.type, self.destinationx, self.destinationy
