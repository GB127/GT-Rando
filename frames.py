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

        isolated_exits = [[19,24],[15,25],[17,19,28,31,7,27,30,43,47],[32,33,34,35,45],[9,10,24,26,36,37,45]] 
        for exit_i in range(self.nExits):
            for isolated_exit in isolated_exits[world_i]:
                if exit_i == isolated_exit:
                    self.exit_to_exits[exit_i] = [exit_i]
                elif isolated_exit in self.exit_to_exits[exit_i]:
                    self.exit_to_exits[exit_i].remove(isolated_exit)

        one_ways = [[],[(16,15),(26,25)],[(28,31),(8,7),(26,27),(29,30),(44,43),(48,47)],[(33,32),(35,34),(46,45),(45,46)],[(10,9),(23,24),(24,23),(26,27),(28,26),(26,28),(37,36),(45,46)]]# start, destination
        for one_way in one_ways[world_i]:
            self.exit_to_exits[one_way[0]].append(one_way[1])

        self.associated_conditions_i, self.conditions_types = self.getAssociatedConditions(world_i)

    def getAssociatedConditions(self, world_i):
        if world_i == 0:
            conditions = [(3,[17,18]),(5,[29]), (7,[11,21])]
            #type of condition: 0: no condition, 1: hook+bridge, 2: hook, 3:bridge, 4: door grey key external, 5: door boss key, 6:double hook, 7: door grey key with no going back!, 8: hook+key
        elif world_i == 1:
            conditions = [(5,[27]),(6,[25,26]),(7,[15]),(7,[19,24])]
        elif world_i == 2:
            conditions = [(3,[22,23]),(4,[39,40]),(5,[53]),(8,[47,48]),(7,[7]),(7,[27]),(7,[30]),(7,[43])]
        elif world_i == 3:
            conditions = [(2,[45,46])] 
            #45 and 46 are treated as one ways towards eachother previously in order to exclude 47 here
        elif world_i == 4:
            conditions = [(2,[3,4]),(2,[18,19]),(2,[19,20]),(2,[23,24]),(5,[41,42]),(6,[43,44]),(8,[26,28])]
            #23 and 24 are treated as one ways towards eachother previously in order to exclude 25 here
            #26 and 28 are treated as one ways towards eachother previously in order to exclude 27 here
        
        associated_conditions_i = []
        conditions_types = [0]
        for this_exit_to_exits in self.exit_to_exits:
            associated_conditions_i.append([0]*len(this_exit_to_exits))

        for condition in conditions:
            conditions_types.append(condition[0])
            condition_i = len(conditions_types)-1
            for source_i in range(len(self.exit_to_exits)):
                for i in range(len(self.exit_to_exits[source_i])):
                    destination_i = self.exit_to_exits[source_i][i]

                    if condition[0] == 7: # NO going back! can cause issues if you arrive there without a key. we should fix this
                        if destination_i in condition[1]:
                            associated_conditions_i[source_i][i] = condition_i

                    elif len(condition[1]) == 1:
                        if destination_i==condition[1][0]:
                            associated_conditions_i[source_i][i] = condition_i
                    elif len(condition[1]) == 2:
                        if destination_i == source_i: pass
                        elif ((source_i in condition[1]) and (destination_i in condition[1])):
                            associated_conditions_i[source_i][i] = condition_i

        return associated_conditions_i, conditions_types

    def getUnlockedExits(self, currently_unlocked, filled_conditions = []):
        new_unlocks = [0]*self.nExits
        if filled_conditions == []:
            for source_i in range(self.nExits):
                if currently_unlocked[source_i]:
                    new_unlocks[source_i] = 1
                    for destination_i in self.exit_to_exits[source_i]:
                        new_unlocks[destination_i] = 1
        else:
            for source_i in range(self.nExits):
                if currently_unlocked[source_i]:
                    new_unlocks[source_i] = 1
                    for i in range(len(self.exit_to_exits[source_i])):
                        destination_i = self.exit_to_exits[source_i][i]
                        associated_condition_i = self.associated_conditions_i[source_i][i]
                        if filled_conditions[associated_condition_i]:
                            new_unlocks[destination_i] = 1

        return new_unlocks