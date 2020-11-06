from getters import getter_items, getter_items_indices
class Items:
    def __init__(self, data, world_i):
        
        all_nFrames = [16, 16, 26, 30, 26]
        self.nFrames = all_nFrames[world_i]
        # getter utilization
        self.offsets,self.values,self.frames = self.getWorldItemsFromData(data,world_i)

    def getWorldItemsFromData(self, data, world_i):
        for frame_i in range(self.nFrames):
            print(self.getFrameItemsFromData(data, world_i, frame_i))

    def getFrameItemsFromData(self, data, world_i, frame_i):
        result = []
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
                    offset5 = data[offset4 + 1] // 2
                    carry = data[offset4 + 1] % 2
                    result.append((offset5, carry))
                offset4 += 4
        if result != []:
            return result
        else:
            return []
