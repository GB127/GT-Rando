class objects:
    def __init__(self, data):
        self.data = data



        self.world_pointers = list(self.data[0x014538:0x014538+5])  # Will never be modified... Could be removed...
        self.level_pointers = []
        for frame_offset in range(0x1453D,0x14620,2):
            self.level_pointers.append(self.data[frame_offset+1] * (16 * 16) + self.data[frame_offset])
            # Reminder for self : For the rewrite, we'll need to decompose.

        self.table = list(self.data[0x14D41:0x15452])


    def save(self):
        # Works, nothing to change here except optimization if you have any...
        tempo_newdata = []
        for pointer in self.level_pointers:
            hi = (pointer & 0xFF00) // 16 // 16
            low = pointer & 0x00FF
            tempo_newdata += [low, hi]
        for no, new_data in enumerate(tempo_newdata):
            self.data[0x1453D + no] = new_data
        for no, new_data in enumerate(self.table):
            self.data[0x14D41 + no] = new_data

    def get_world_frame(self, world_i, frame_i):
        world_nframes = [0, 16, 32, 58, 88]
        level_pointer = self.level_pointers[world_nframes[world_i] + frame_i] - 0xCD41
        count = self.table[level_pointer]
        objects = []
        for objec in range(count):
            ID = (self.table[level_pointer+1 + 3*objec])
            objects.append([ID, self.transform_byt_co(self.table[level_pointer+2 + 3*objec], self.table[level_pointer+1 + 3*objec])])
        print(objects)

    def transform_byt_co(self, big_value):
        assert big_value % 2 == 0, "Cannot be an impair number"
        y = ( big_value // 0x40) / 2
        x = (big_value % 0x40) / 2
        assert x < 31 and 0 < x, "Cannot use this byte"
        return x, y

    def transform_co_byt(self, x, y):
        assert x <= 30 and 0 < x, f"X cannot be {x}."
        #TODO : Y
        assert x % 0.5 == 0 and y % 0.5 ==0 , "X or Y cannot be this value, can only be a multiple of 0.5"
        transfo_y = y * 2 * 0x40
        big_value = transfo_y + x * 2
        return int(big_value)



    def add_objects(self, world_i, frame_i, object_ids, objects_co):
        world_nframes = [0, 16, 32, 58, 88]
        level_pointer = self.level_pointers[world_nframes[world_i] + frame_i] - 0xCD41
        self.table[level_pointer] += len(object_ids)
        for no, objec in enumerate(object_ids):
            tempo_big = self.transform_co_byt(objects_co[no][0], objects_co[no][1])
            tempo_hi = (tempo_big & 0xFF00) // 16 // 16
            tempo_low = (tempo_big & 0xFF)

            self.table.insert(level_pointer + 1, tempo_hi)
            self.table.insert(level_pointer + 1, tempo_low)
            self.table.insert(level_pointer + 1, objec)


        #Pointers fix
        self.level_pointers[level_pointer+1:] = [x + 3*len(object_ids) for x in self.level_pointers[level_pointer+1:]]



    def clear_frame(self, world_i, frame_i):
        # Works, nothing to change here.
        world_nframes = [0, 16, 32, 58, 88]
        level_pointer = self.level_pointers[world_nframes[world_i] + frame_i] - 0xCD41
        count = self.table[level_pointer]
        self.table[level_pointer] = 0
        for _ in range(count * 3):
            self.table.pop(level_pointer+1)

        #Pointers fix
        self.level_pointers[level_pointer+1:] = [x - 3*count for x in self.level_pointers[level_pointer+1:]]