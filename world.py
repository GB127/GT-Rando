import random
from copy import deepcopy
from getters import getter_exits


class World():
    def __init__(self, data, world_i):
        assert isinstance(data, bytearray), "Must be a bytearray"
        assert 0 <= world_i <= 4, "Must be in range 0-4."

        all_nFrames = [16, 16, 26, 30, 26]
        all_bossFrame = [14, 15, 25, 25, 25]
        all_preBossFrame = [12, 14, 24, 24, 24]
        self.world_i = world_i
        self.data = data
        self.nFrames = all_nFrames[world_i]
        self.bossFrame = all_bossFrame[world_i]
        self.exits_offsets, self.exits_values, self.source_frames = getter_exits(data, world_i, self.nFrames)
        self.destination_frames = []
        self.destination_pos = []

        for this_exit_values in self.exits_values:
            self.destination_frames.append(this_exit_values[0])
            if this_exit_values[4]<25:
                self.destination_pos.append('W')
            elif this_exit_values[4]>230:
                self.destination_pos.append('E')
            elif this_exit_values[5]<40:
                self.destination_pos.append('N')
            elif this_exit_values[5]>190:
                self.destination_pos.append('S')
            else:
                self.destination_pos.append('?')

        for i,this_exit_values in enumerate(self.exits_values):
                if this_exit_values[0] == self.bossFrame:
                    self.preboss_index = i
                    break

        self.exit_pairs = []
        for i,source in enumerate(self.source_frames):
            for j,destination in enumerate(self.destination_frames):
                if (self.destination_frames[i] == self.source_frames[j])&(self.destination_frames[j] == self.source_frames[i]):
                    if sorted([i,j]) not in self.exit_pairs: 
                        self.exit_pairs.append(sorted([i,j]))

        self.nExits = len(self.source_frames)


    def randomize_exits(self, fix_boss_exit, keep_direction, pair_exits): #fix_boss_exit is a bool
        
        #determine new order
        if keep_direction & (not pair_exits):#keep direction
            new_order = list(range(self.nExits))
            for ref_destination_pos in ['N','S','W','E']:
                i_to_shuffle_now = [i for i, this_destination_pos in enumerate(self.destination_pos) if this_destination_pos == ref_destination_pos]
                if fix_boss_exit: 
                    if self.preboss_index in i_to_shuffle_now: i_to_shuffle_now.remove(self.preboss_index)
                shuffled_i = deepcopy(i_to_shuffle_now)
                random.shuffle(shuffled_i)
                for j,i in enumerate(i_to_shuffle_now):
                    new_order[i] = shuffled_i[j]

        elif (not keep_direction) & (pair_exits):#pair exits
            new_order = list(range(self.nExits))
            shuffled_pairs = deepcopy(self.exit_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(self.exit_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]

        elif keep_direction & pair_exits: #keep direction AND pair exits
            new_order = list(range(self.nExits))
            pairs_to_sort = deepcopy(self.exit_pairs)
            NS_pairs = []
            WE_pairs = []
            for pair in pairs_to_sort:
                if (self.destination_pos[pair[0]] == 'N') or (self.destination_pos[pair[0]] == 'S'):
                    NS_pairs.append(pair)
                elif (self.destination_pos[pair[0]] == 'W') or (self.destination_pos[pair[0]] == 'E'):
                    WE_pairs.append(pair)
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

        else: #totally random
            new_order = list(range(self.nExits))
            random.shuffle(new_order)
            if fix_boss_exit:
                new_order.remove(self.preboss_index)
                new_order.insert(self.preboss_index,self.preboss_index)
            

        #assign elements in new order
        old_exits_values = deepcopy(self.exits_values)
        for i,temp in enumerate(old_exits_values):
            self.exits_values[i][0] = old_exits_values[new_order[i]][0]
            self.exits_values[i][4] = old_exits_values[new_order[i]][4]
            self.exits_values[i][5] = old_exits_values[new_order[i]][5]

        return self.exits_values
