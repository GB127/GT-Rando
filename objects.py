class objects:
    def __init__(self, data):
        self.data = data


    def remove_stars(self,world_i, frame_i):
        # remove all star blocks from world-frame in question.
        values_else, stars_count = [], 0
        world_pointer = self[0x014538 + world_i]
        level_pointer = self[0x14538 + 1 + world_pointer + 2*frame_i] * (16 * 16) + self[0x14538 + world_pointer + 2*frame_i]
        offset = 0x8000 + level_pointer
        count = self[offset]
        for item in range(count):
            if self[offset +1 + item*3] == 0x1A:
                stars_count += 1
            else:
                values_else += [self[offset +1 + item*3], self[offset +2 + item*3], self[offset +3 + item*3]]
        new_values = [count -(1 * stars_count)] + values_else
        old_values = list(self[offset +1 + (3*count):0x15454])
        self.rewrite(offset, new_values + old_values)

        # Fixing the next pointers:
        for offset in range(0x01453D + 2*[0, 16, 32, 58, 88][world_i] + 2*(frame_i+1), 0x014621, 2):
            try:
                self[offset] -= stars_count * 0x3
            except ValueError:
                self[offset] = self[offset] - stars_count * 0x3 + 256
                self[offset+1] -= 0x1


    def add_stars(self, world_i, frame_i, coordinates):
        values_stars = []
        for coordinate in coordinates:
            values_stars += [0x1A, coordinate&0xFF, (coordinate&0xFF00) // 16 // 16]
        values_else= []
        world_pointer = self[0x014538 + world_i]
        level_pointer = self[0x14538 + 1 + world_pointer + 2*frame_i] * (16 * 16) + self[0x14538 + world_pointer + 2*frame_i]
        offset = 0x8000 + level_pointer
        count = self[offset]
        for item in range(count):
            if self[offset +1 + item*3] == 0x1A:
                values_stars += [self[offset +1 + item*3], self[offset +2 + item*3], self[offset +3 + item*3]]
            else:
                values_else += [self[offset +1 + item*3], self[offset +2 + item*3], self[offset +3 + item*3]]
        new_values = [count +len(coordinates)] + values_else + values_stars
        old_values = list(self[offset +1 + (3*count):0x15452])
        self.rewrite(offset, new_values + old_values)

        # Fixing the next pointers:
        for offset in range(0x01453D + 2*[0, 16, 32, 58, 88][world_i] + 2*(frame_i+1), 0x014621, 2):
            try:
                self[offset] += 0x3 * len(coordinates)
            except ValueError:
                self[offset] += 0x3 * len(coordinates) - 256
                self[offset+1] += 0x1





