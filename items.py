import random

class Items:
    def __init__(self, data, world_i):
        all_nFrames = [16, 16, 26, 30, 26] # Nb of frames per world.
        self.nFrames = all_nFrames[world_i]  # Get the current world's number of frames

        # getter utilization
        self.offsets, self.values = self.getItemsFromData(data,world_i)
        self.names = self.getNames()
        self.frames = self.getCorrespondingFramesFromData(data,world_i)
        self.nItems = len(self.offsets)

        self.associated_exits, self.associated_conditions, self.conditions_types = self.getAssociatedExits(world_i)


    def set_item(self, item_i, value):
        self.values[item_i] = value


    def __str__(self):
        conditions = {0: "no condition", 1: "hook + bridge", 2: "hook", 3:"bridge", 4: "door grey key external", 5: "door boss key", 6:"double hook"}

        result = ""
        for no, item in enumerate(self.getNames()):
            result += f'   {no:<2}| {item:9}| frame {self.frames[no]:2} | Exit # {self.associated_exits[no]:2} |  {conditions[self.associated_conditions[no]]}\n'
        return result

    def getAssociatedExits(self, world_i):
        if world_i == 0:
            associated_exits = [2,5,7,10,12,19,24,28,30,31]  # Note for GB : The logic progresses from exits to exits. Not frames to frames.
            associated_conditions = [0,0,0,0,0,0,0,0,0,0]
            conditions_types = [0]
        elif world_i == 1:
            associated_exits = [7,9,9,13,14,14,16,16,22,24,24,25]
            associated_conditions = [0,0,0,0,1,1,2,2,0,0,0,0] #index of associated condition to reach the item
            conditions_types = [0,1,2]
            #type of condition: 0: no condition, 1: hook+bridge, 2: hook, 3:bridge, 4: door grey key external, 5: door boss key, 6:double hook
        elif world_i == 2:
            associated_exits = [6,8,10,10,10,13,13,22,22,22,26,32,35,37,39,44,44,47,48,47,52]
            associated_conditions = [0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0] #index of associated condition to reach the item
            conditions_types = [0,3,2]
        elif world_i == 3:
            associated_exits = [8,8,23,39,42]
            associated_conditions = [0,0,0,0,0] #index of associated condition to reach the item
            conditions_types = [0]
        elif world_i == 4:
            associated_exits = [3,13,13,17,17,24,23,29,29,29,30,33,33,34,36,42,48,48]
            associated_conditions = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #index of associated condition to reach the item
            conditions_types = [0]
        return associated_exits, associated_conditions, conditions_types

    def getUnlockedItems(self, unlocked_exits, filled_conditions):
        unlocked_items = [0]*self.nItems
        for source_i in range(len(unlocked_exits)):
            if unlocked_exits[source_i]:
                for item_i in range(len(self.associated_exits)):
                    associated_exit = self.associated_exits[item_i]
                    associated_condition = self.associated_conditions[item_i]
                    if associated_exit == source_i:
                        if filled_conditions[associated_condition]:
                            unlocked_items[item_i] = 1

        return unlocked_items

    def getNames(self):
        # GB : Petite suggestion de code.
        # all_names = ["Hookshot","Candle","Grey Key","Gold Key","Shovel","Bell","Bridge"]
        all_names = {0x8 : "Hookshot", 0x9 : "Candle", 0xA : "Grey Key",0xB : "Gold Key", 0xC :"Shovel", 0xD : "Bell", 0xE : "Bridge"}
        names = []
        for value in self.values:
            # names.append(all_names[value-8])
            names.append(all_names[value])
        return names

    def randomize(self, only_switch_positions):
        if only_switch_positions: 
            random.shuffle(self.values)
        else: #totally random
            self.values = [random.randint(8,14) for i in self.values]
        self.names = self.getNames()

    def getItemsFromData(self, data, world_i):
        items_offsets = []
        items_values = []
        n_sections_to_read = data[0x66D6 + world_i]
        offset = data[0x6E6A + data[0x6E6A + world_i] + 1]*16*16 + data[0x6E6A + data[0x6E6A + world_i]] - 0x8000
        for i in range(n_sections_to_read):
            n_elem_to_read = data[offset]
            offset += 1
            for j in range(n_elem_to_read):
                verification = data[offset] & 0xE0
                if verification == 0:
                    # Pas de byte à gauche (Donc on a 0x00 à 0x0F)
                    items_offsets.append(offset)
                offset += 4  # E55A

        for item_offset in items_offsets:
            items_values.append(data[item_offset])

        return items_offsets, items_values

    def getCorrespondingFramesFromData(self, data, world_i):
        frames = []
        for frame_i in range(self.nFrames):
            offset1 = 2* frame_i + data[world_i + 0x6E6A]
            offset2 = data[offset1 + 0x6E6A]
            offset3 = data[offset1 + 0x6E6A + 1]
            offset4 = offset3 * 16 * 16 + offset2 - 0x8000
            count = data[offset4]
            if count != 0:
                offset4 += 1
                for _ in range(count):
                    X = data[offset4]
                    X = X & 0xE0
                    X = X // 16
                    if X == 0x0:
                        frames.append(frame_i)
                    offset4 += 4
        
        return frames
