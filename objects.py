class objects:
    def __init__(self, data):
        self.data = data



        self.world_pointers = list(self.data[0x014538:0x014538+5])  # Will never be modified... Could be removed...
        self.level_pointers = []
        for frame_offset in range(0x1453D,0x14620,2):
            self.level_pointers.append(self.data[frame_offset+1] * (16 * 16) + self.data[frame_offset])
            # Reminder for self : For the rewrite, we'll need to decompose.

        self.table = list(self.data[0x14D41:0x15452])

    def get_world_frame(self, world_i, frame_i):
        world_nframes = [0, 16, 32, 58, 88]
        level_pointer = self.level_pointers[world_nframes[world_i] + frame_i] - 0xCD41
        count = self.table[level_pointer]
        objects = []
        for objec in range(count):
            ID = (self.table[level_pointer+1 + 3*objec])
            objects.append([ID, self.transform_byt_co(self.table[level_pointer+2 + 3*objec], self.table[level_pointer+1 + 3*objec])])
        print(objects)

    def transform_byt_co(self, hi_byte, low_byte):
        big_value = hi_byte * 16 * 16 + low_byte
        # These values will have ot be adjusted as they are wrong, but it's a start.
        y = big_value // 0x80
        x = big_value % 16
        return x, y


    def clear_frame(self, world_i, frame_i):
        world_nframes = [0, 16, 32, 58, 88]
        level_pointer = self.level_pointers[world_nframes[world_i] + frame_i] - 0xCD41
        count = self.table[level_pointer]
        self.table[level_pointer] = 0
        for _ in range(count * 3):
            self.table.pop(level_pointer+1)

        #TODO: fix pointers 



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





