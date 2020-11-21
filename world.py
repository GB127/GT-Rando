import random
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle
import cv2
import numpy as np
from exits import *
from items import *
from frames import *

class World():
    def __init__(self, data, world_i, starting_exit=0):
        assert isinstance(data, bytearray), "Must be a bytearray"
        assert 0 <= world_i <= 4, "Must be in range 0-4."

        all_nFrames = [16, 16, 26, 30, 26]
        starting_frame_offsets = list(range(0x1FFA7, 0x1FFAC))

        self.starting_frame_offset = starting_frame_offsets[world_i]
        self.world_i = world_i
        self.data = data
        self.nFrames = all_nFrames[world_i]
        self.exits = Exits(data, world_i)
        self.nExits = len(self.exits.offsets)
        self.original_exits = deepcopy(self.exits)
        self.items = Items(data, world_i)
        self.nItems = len(self.items.offsets)
        self.frames = Frames(data, world_i, self.exits.source_frames, self.items.frames)

        self.starting_exit = starting_exit
        self.initial_frame_coordinates_offsets = self.get_initial_frame_coordinates_offsets_from_data()

        print('World ',world_i, ' created!')

    def randomize_firstframe(self):
        boss_exit = self.exits.boss_exit
        all_exits = list(range(self.nExits))
        all_exits.pop(boss_exit)
        starting_exit = random.choice(all_exits)
        self.starting_frame = self.exits.source_frames[starting_exit]
        initial_frame_coordinates_offsets, initial_frame_coordinates = self.set_starting_exit(starting_exit)
        return initial_frame_coordinates_offsets, initial_frame_coordinates

    def set_starting_exit(self, starting_exit):
        self.starting_exit = starting_exit
        [offset_x_goofy, offset_y_goofy, offset_x_max, offset_y_max] = self.initial_frame_coordinates_offsets
        if starting_exit == 0:
            return [offset_x_goofy, offset_y_goofy, offset_x_max, offset_y_max], [self.data[offset_x_goofy], self.data[offset_y_goofy], self.data[offset_x_max], self.data[offset_y_max]]
        else:
            return [offset_x_goofy, offset_y_goofy, offset_x_max, offset_y_max], [self.exits.source_Xpos[starting_exit], self.exits.source_Ypos[starting_exit], self.exits.source_Xpos[starting_exit], self.exits.source_Ypos[starting_exit]]


    def get_initial_frame_coordinates_offsets_from_data(self):
        world_offset = self.world_i * 2 * 2
        offset_x_goofy = 0x1867B + world_offset
        offset_y_goofy = 0x1867B + world_offset + 1
        offset_x_max = 0x1867B + world_offset + 2
        offset_y_max = 0x1867B + world_offset + 3

        return [offset_x_goofy, offset_y_goofy, offset_x_max, offset_y_max]

    def showMap(self, show_exits=True, show_items=True):
        #map
        filenames = ['map0.png','map1.png','map2.png','map3.png','map4.png']
        img = cv2.imread('maps/'+filenames[self.world_i])
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
        frame_positions = all_worlds_frame_positions[self.world_i]
        for frame_i in range(self.nFrames):
            base_pos = frame_positions[frame_i]
            ax.add_patch(Circle((base_pos[0],base_pos[1]),24, color='w'))
            ax.text(base_pos[0],base_pos[1],str(frame_i),fontsize=11,
                    horizontalalignment='center', verticalalignment='center')

            if show_items:#items
                if frame_i in self.items.frames: 
                    item_i = [i for i, x in enumerate(self.items.frames) if x == frame_i] #items in this frame
                    item_name = [self.items.names[i] for i in item_i]
                    ax.text(base_pos[0],base_pos[1]+40,str(item_i),fontsize=7,
                        horizontalalignment='center', verticalalignment='center', color='w')
                    ax.text(base_pos[0],base_pos[1]+65,str(item_name),fontsize=5,
                        horizontalalignment='center', verticalalignment='center', color='w')

        
        #exits
        if show_exits:
            for i,source in enumerate(self.exits.source_frames):
                this_color = list(1-np.random.choice(range(256), size=3)/300)
                #source exit
                base_pos = frame_positions[source]
                source_pos = (base_pos[0]-frame_size[0]/2+self.exits.source_Xpos[i], base_pos[1]-frame_size[1]/2+self.exits.source_Ypos[i])
                ax.add_patch(Circle(source_pos,5, color=this_color))
                ax.text(source_pos[0],source_pos[1],str(i),fontsize=10,
                        horizontalalignment='center', verticalalignment='center', color='red')
                #target exit
                base_pos = frame_positions[self.exits.destination_frames[i]]
                target_pos = (base_pos[0]-frame_size[0]/2+self.exits.destination_Xpos[i], base_pos[1]-frame_size[1]/2+self.exits.destination_Ypos[i])
                ax.arrow(source_pos[0],source_pos[1],target_pos[0]-source_pos[0], target_pos[1]-source_pos[1], 
                        head_width=15,length_includes_head=True, color=this_color)

        plt.show()
        return ''

    def feasibleWorldVerification(self):
        unlocked_exits = [0]*self.nExits
        unlocked_exits[self.starting_exit] = 1 #means that we have access to this exit at the start
        used_items = [0]*self.nItems
        items_filled_conditions = [0]*len(self.items.conditions_types) #means that we already put none of the the bridges and hooks to reach the items
        items_filled_conditions[0] = 1 # element 0 should always be set to 1 in this list
        frames_filled_conditions = [0]*len(self.frames.conditions_types) #means that we already put none of the the bridges and hooks to reach the exits
        frames_filled_conditions[0] = 1 # element 0 should always be set to 1 in this list
        for big_step in range(50): #max number or loops
            for small_step in range(random.randint(2, 8)): #how much exploration before we unlock something
                #exits links
                unlocked_exits, boss_reached = self.exits.getUnlockedExits(unlocked_exits)
                #internal frame links
                unlocked_exits = self.frames.getUnlockedExits(unlocked_exits, frames_filled_conditions)
            #unlocked items
            unlocked_items = self.items.getUnlockedItems(unlocked_exits, items_filled_conditions)

            #We now have to unlock something in order to move further?
            #what can we unlock right now?
            frames_reachable_conditions, items_reachable_conditions = self.getReachableConditions(unlocked_exits, frames_filled_conditions, items_filled_conditions)
            frames_unlockable_conditions, items_unlockable_conditions = self.getUnlockableConditions(frames_reachable_conditions, items_reachable_conditions, unlocked_items, used_items)
            #randomly chose which condition to unlock
            if len(frames_unlockable_conditions)+len(items_unlockable_conditions)>0:
                random_i = random.randint(0, len(frames_unlockable_conditions)+len(items_unlockable_conditions)-1)
                if random_i<len(frames_unlockable_conditions): #we unlock a frame condition
                    condition_i = frames_unlockable_conditions[random_i]
                    frames_filled_conditions, used_items = self.unlockAFrameCondition(condition_i, frames_filled_conditions, unlocked_items, used_items)
                else: #we unlock an item condition
                    random_i = random_i-len(frames_unlockable_conditions)
                    condition_i = items_unlockable_conditions[random_i]
                    items_filled_conditions, used_items = self.unlockAnItemCondition(condition_i, items_filled_conditions, unlocked_items, used_items)

            #verify if the world is completed
            if all(unlocked_exits) and all(unlocked_items) and boss_reached:
                break

        return unlocked_exits, unlocked_items, boss_reached


    def unlockAFrameCondition(self, condition_i, frames_filled_conditions, unlocked_items, used_items):
        condition_type = self.frames.conditions_types[condition_i]
        frames_filled_conditions[condition_i] = 1

        if (condition_type == 1): required_items = [0x8,0xE]
        elif (condition_type == 2): required_items = [0x8]
        elif (condition_type == 3): required_items = [0xE]
        elif (condition_type == 4): required_items = [0xA]
        elif (condition_type == 5): required_items = [0xB]
        elif (condition_type == 6): required_items = [0x8,0x8]
        elif (condition_type == 7): required_items = [0xA]
        elif (condition_type == 8): required_items = [0x8,0xA]
        for required_item in required_items:
            for item_i in range(self.nItems):
                if unlocked_items[item_i] and not used_items[item_i]:
                    used_items[item_i] = 1 #we use that item
                    break

        return frames_filled_conditions, used_items
        

    def unlockAnItemCondition(self, condition_i, items_filled_conditions, unlocked_items, used_items):
        condition_type = self.items.conditions_types[condition_i]
        items_filled_conditions[condition_i] = 1

        if (condition_type == 1): required_items = [0x8,0xE]
        elif (condition_type == 2): required_items = [0x8]
        elif (condition_type == 3): required_items = [0xE]
        elif (condition_type == 4): required_items = [0xA]
        elif (condition_type == 5): required_items = [0xB]
        elif (condition_type == 6): required_items = [0x8,0x8]
        elif (condition_type == 7) and (0xA in available_items): frames_unlockable_conditions.append(condition_i)
        elif (condition_type == 8): required_items = [0x8,0xA]

        for required_item in required_items:
            for item_i in range(self.nItems):
                if unlocked_items[item_i] and not used_items[item_i]:
                    used_items[item_i] = 1 #we use that item
                    break

        return items_filled_conditions, used_items
        
    
    def getUnlockableConditions(self, frames_reachable_conditions, items_reachable_conditions, unlocked_items, used_items):
        available_items = []
        for item_i in range(self.nItems):
            if unlocked_items[item_i] and not used_items[item_i]:
                available_items.append(self.items.values[item_i])

        frames_unlockable_conditions = []
        for i in range(len(frames_reachable_conditions)):
            condition_i = frames_reachable_conditions[i]
            condition_type = self.frames.conditions_types[condition_i]
            #type of condition: 0: no condition, 1: hook+bridge, 2: hook, 3:bridge, 4: door grey key external, 5: door boss key, 6:double hook, 7: door grey key with no going back!, 8: hook+key
            #{0x8 : "Hookshot", 0x9 : "Candle", 0xA : "Grey Key",0xB : "Gold Key", 0xC :"Shovel", 0xD : "Bell", 0xE : "Bridge"}
            if (condition_type == 1) and (0x8 in available_items) and (0xE in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 2) and (0x8 in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 3) and (0xE in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 4) and (0xA in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 5) and (0xB in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 6) and (available_items.count(0x8)>=2): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 7) and (0xA in available_items): frames_unlockable_conditions.append(condition_i)
            elif (condition_type == 8) and (0x8 in available_items) and (0xA in available_items): frames_unlockable_conditions.append(condition_i)
        
        items_unlockable_conditions = []
        for i in range(len(items_reachable_conditions)):
            condition_i = items_reachable_conditions[i]
            condition_type = self.items.conditions_types[condition_i]
            #type of condition: 0: no condition, 1: hook+bridge, 2: hook, 3:bridge, 4: door grey key external, 5: door boss key, 6:double hook, 7: door grey key with no going back!, 8: hook+key
            #{0x8 : "Hookshot", 0x9 : "Candle", 0xA : "Grey Key",0xB : "Gold Key", 0xC :"Shovel", 0xD : "Bell", 0xE : "Bridge"}
            if (condition_type == 1) and (0x8 in available_items) and (0xE in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 2) and (0x8 in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 3) and (0xE in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 4) and (0xA in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 5) and (0xB in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 6) and (available_items.count(0x8)>=2): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 7) and (0xA in available_items): items_unlockable_conditions.append(condition_i)
            elif (condition_type == 8) and (0x8 in available_items) and (0xA in available_items): items_unlockable_conditions.append(condition_i)

        return frames_unlockable_conditions, items_unlockable_conditions


    def getReachableConditions(self, unlocked_exits, frames_filled_conditions, items_filled_conditions): 
        # A place where you can use a bridge or a hook is called a condition. 
        # There are conditions to unlocks items and conditions to unlock exits inside a given frame
        # This function checks which of these conditions are reachable
        frames_reachable_conditions = []
        items_reachable_conditions = []
        for exit_i in range(len(unlocked_exits)):
                if unlocked_exits[exit_i]:
                    for condition_i in self.frames.associated_conditions_i[exit_i]:
                        if condition_i not in frames_reachable_conditions:
                            frames_reachable_conditions.append(condition_i)
                    for item_i in range(self.nItems):
                        associated_exit_i = self.items.associated_exits[item_i]
                        if exit_i == associated_exit_i:
                            condition_i = self.items.associated_conditions[item_i]
                            if condition_i not in items_reachable_conditions:
                                items_reachable_conditions.append(condition_i)

        # remove conditions that are already met
        for condition_i in range(len(frames_filled_conditions)):
            if frames_filled_conditions[condition_i]:
                if condition_i in frames_reachable_conditions:
                    frames_reachable_conditions.remove(condition_i)
        for condition_i in range(len(items_filled_conditions)):
            if items_filled_conditions[condition_i]:
                if condition_i in items_reachable_conditions:
                    items_reachable_conditions.remove(condition_i)

        return frames_reachable_conditions, items_reachable_conditions 


    def allFramesConnectedVerification(self, starting_exit=0):
        unlocked_exits = [0]*self.nExits
        unlocked_exits[starting_exit] = 1
        frames_filled_conditions = [1]*len(self.frames.conditions_types) #means that we already put all the bridges and hooks to reach the exits
        for step in range(50): #max number or loops
            #exits links
            unlocked_exits, boss_reached = self.exits.getUnlockedExits(unlocked_exits)
            #internal frame links
            unlocked_exits = self.frames.getUnlockedExits(unlocked_exits, frames_filled_conditions)
        return all(unlocked_exits)