import random
from copy import deepcopy

class Frames:
    def __init__(self, data, world_i, exits_frames, items_frames):
        
        all_nFrames = [16, 16, 26, 30, 26]
        self.nFrames = all_nFrames[world_i]
        self.nExits = len(exits_frames)
        
        self.exits = []
        self.items = []
        for frame_i in range(self.nFrames):
            self.exits.append([i for i, x in enumerate(exits_frames) if x == frame_i]) #exits in this frame
            self.items.append([i for i, x in enumerate(items_frames) if x == frame_i]) #items in this frame
        
        self.exit_to_exits = []
        self.exit_to_items = []
        for exit_i in range(self.nExits):
            for frame_i in range(self.nFrames):
                if exit_i in self.exits[frame_i]: #exit_i is in frame_i
                    self.exit_to_exits.append(deepcopy(self.exits[frame_i])) #exit_i unlocks these exits
                    self.exit_to_items.append(deepcopy(self.items[frame_i])) #exit_i unlocks these items

        isolated_exits = [[19,24],[],[17,19,28,31],[32,33,34,35],[9,10,23,24,36,37,45,46]] 
        for exit_i in range(self.nExits):
            for isolated_exit in isolated_exits[world_i]:
                if exit_i == isolated_exit:
                    self.exit_to_exits[exit_i] = [exit_i]
                elif isolated_exit in self.exit_to_exits[exit_i]:
                    self.exit_to_exits[exit_i].remove(isolated_exit)

        one_ways = [[],[],[(28,31)],[(33,32),(35,34)],[(10,9),(37,36),(23,24),(4,45,46)]]# world, start, destination
        for one_way in one_ways[world_i]:
            self.exit_to_exits[one_way[0]].append(one_way[1])

        self.original_exit_to_exits = deepcopy(self.exit_to_exits) #this assumes that you always have access to any item

        exits_blocked_by_bridge = [[17],[],[23],[],[]]
        exits_blocked_by_door = [[11,21],[15000],[7000,27000,30000,43000,47000,40],[],[26000]]
        exits_blocked_by_bossdoor = [[29],[27],[53],[],[41,42]]
        exits_blocked_by_hook = [[],[],[48],[],[4,18,20,26]]
        exits_blocked_by_double_hook = [[],[25],[],[],[44]]


        

    