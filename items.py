import random

class Items:
    def __init__(self, data, world_i):
        all_nFrames = [16, 16, 26, 30, 26]
        self.nFrames = all_nFrames[world_i]
        # getter utilization
        self.offsets, self.values = self.getItemsFromData(data,world_i)
        self.frames = self.getCorrespondingFramesFromData(data,world_i)
        self.nItems = len(self.offsets)
        self.names = self.getNames()

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
