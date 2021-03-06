import random
from copy import deepcopy

class objects:
    grabable = [x for x in range(0, 0x1A, 2)]
    kickable = [x for x in range(0x1A, 0x22, 2)]
    ID = {
        0x0 : "Baril",
        0x2 : "Amphore",
        0x4 : "Egg",
        0x6 : "Sign",
        0x8 : "Plant",
        0xA : "Bomb",
        0xC : "Log",
        0xE : "2 logs",
        0x10 : "Icy thing?",
        0x12 : "coquillage",
        0x14 : "Trash can?",
        0x16 : "Gray Rock",
        0x18 : "Vanilla rock",
        0x1A : "Star block",
        0x1C : "Greeen bombable stone",
        0x1E : "Orange bombable stone",
        0x20 : "Red bombable stone"
        }        #NOTE : Didn't try higher than 0x50


    jap1 = [
            [  # World 0
                (   [],
                    []),  # 0-0
                (
                    [],
                    []),  # 0-1
                (   [0x18, 0x18, 0x18, 0x1A, 0x1A],
                    [(2,3),(2,7),(13,7),(6,10),(9,10)]),  # 0-2
                (   [0x1A, 0x1A, 0x1A, 0x1A, 0x1A],
                    [(3,5),(11,7),(12,8),(13,8),(13,9)]),  # 0-3
                (   [0x0, 0x0, 0x0, 0x2, 0x2, 0x8, 0x8, 0x8,0x8],
                    [(1.5,5),(2.5, 5),(2.5, 4),(13,11),(14,10),(6.5, 5),(7.4,5),(6.5,9),(7.5,9)]),  # 0-4
                (   [0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x1A, 0x18],
                    [(3,3),(4,3),(5,3),(6,3),(7,3), (10,4),(12,4), (6,10),( 6,11),(6, 12),(9,9),(9,10),(9,11),(6,9),(1,9)]),  # 0-5
                (   [0x8, 0x8, 0x8, 0x1A, 0x1A, 0x1A],
                    [(9,7),(7,10),(8,10),(3,8), (8,4), (12,8)]),  # 0-6
                (   [0x4],
                    [(14,2)]),  # 0-7
                (   [0x18 for _ in range(5)],
                    [(1.5,12),(6.5, 5),(13.5, 2),(14,11),(14,12)]),  # 0-8
                (   [0x0,0x0,0x0, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8],
                    [(1,12),(4,12),(8,9), (11, 10),(12, 10),(14,8),(14,9),(14, 10),(14, 11),(14,12)]),  # 0-9
                (   [0x8 for _ in range(10)],
                    [(1,3),(2,11),(2,12),(5,6),(5,7),(5,8),(5,9),(10,3),(10,4),(12,11)]),  # 0-10
                (   [0x1A for _ in range(4)],
                    [(6,7),(5,8),(10,8),(13,6)]), # 0-11
                (   [0x1A for _ in range(2)],
                    [(6,9),(12.5, 4)]),  # 0-12
                (   [0x1A for _ in range(6)],
                    [(4,9),(4,10),(6,7),(8,7),(10,9),(11,6)]),  # 0-13
                (   [0x0 for _ in range(4)],
                    [(1,8),(14,8),(1.5, 12),(13.5, 12)]),  # 0-14
                (   [0x0, 0x0, 0x0, 0x8, 0x8, 0x8,0x8,0x8,0x8,0x8,0x8,0x1A], 
                    [(1,4),(1,12),(2,12),(12,6),(12,7),(12,8),(12,9),(12,10),(3,12),(4,12),(5,12),(14,9)])  # 0-15
                ]
            ,
            [  # World 1
                (   [0x1A, 0x1A, 0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0],
                    [(6,6),(9,6), (7,5),(8,5),(5,7),(5,8),(4,8),(10,7),(10,8),(11,8)]),  # World 1-0
                (   [],
                    []), # 1-0
                (   [0xA for _ in range(4)],
                    [(3,8),(8,8),(9,8),(10,9)]),  # 1-2
                (   [0x8 for _ in range(7)],
                    [(6,11),(8,11),(5,4),(5,5),(5,6),(10,11),(7,8)]),  # 1-3
                (   [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1A, 0x1A], 
                    [(1,2),(8,11),(8,12),(12,9),(7,4),(9,4),(8,7),(8,8)]),  # 1-4
                (   [0x8, 0x8],
                    [(6,6),(8,8)]),  # 1-5
                (   [0x8, 0x8, 0x8, 0x8,0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C],
                    [(1,8),(5,10),(10,12),(11,12), (2,6),(5,8),(5,11),(4,11),(10,4),(11,4)]),  # 1-6
                (   [0x8 for _ in range(3)],
                    [(11,3),(12,4),(12,12)]), # 1-7
                (   [0x8 for _ in range(7)],
                    [(2,2),(3,2),(5,12),(6,12),(11,4),(12,3),(12,2)]),  # 1-8
                (   [0x1A, 0x1A, 0x1C, 0x1C, 0x1C, 0x1C],
                    [(7,4),(11,4),(2,5),(4,7),(10,8),(12,10)]),  # 1-9
                (   [],
                    []),  # 1-10
                (   [0x0 for _ in range(8)],
                    [(1,2),(2,2),(3,2),(4,2),(4,3),(6,6),(6,8),(7,8)]),  # 1-11
                (   [0x0 for _ in range(5)],
                    [(1,12),(2,12),(4,12),(5,12),(13,10)]),  # 1-12
                (   [0x0],
                    [(1,12)]),  # 1-13
                (   [],
                    []), # 1-14
                (   [0x0 for _ in range(4)], 
                    [(2.5,11),(2.5, 12),(12.5,11),(12.5, 12)])  # 1-15
                    ]
















    ]
















    def __init__(self, data):
        self.data = data



        self.world_pointers = list(self.data[0x014538:0x014538+5])  # Will never be modified... Could be removed...
        self.level_pointers = []
        for frame_offset in range(0x1453D,0x14620,2):
            self.level_pointers.append(self.data[frame_offset+1] * (16 * 16) + self.data[frame_offset])

        self.table = list(self.data[0x14D41:0x15452])


    def randomize_grabables(self):
        grabable_rando = deepcopy(objects.grabable)
        random.shuffle(grabable_rando)
        for frame in self.level_pointers:
            count = self.table[frame - 0xCD41]
            for x in range(count):
                current_index = frame - 0xCD41 + 1 + 3*x
                if self.table[current_index] in objects.grabable:
                    self.table[current_index] = grabable_rando[objects.grabable.index(self.table[current_index])]
    
        self.write_data()


    def print_world(self, world_i, frame_i):

        ID_string = {
            0x0 : "WW",
            0x2 : "AA",
            0x4 : "EE",
            0x6 : "SS",
            0x8 : "PP",
            0xA : "BB",
            0xC : "LL",
            0xE : "22",
            0x10 : "II",
            0x12 : "CC",
            0x14 : "TT",
            0x16 : "RR",
            0x18 : "rr",
            0x1A : "XX",
            0x1C : "GG",
            0x1E : "OO",
            0x20 : "RR"
            }        #NOTE : Didn't try higher than 0x50








        boundary_top = "_" * 34
        boundary_bottom = "¯" * 34
        string_list = []
        for _ in range(28):
            string_list.append("|" + " " * 32 + "|")

        for one in self.get_world_frame(world_i, frame_i):
            x = int(2*one[1][0])
            y = int(2*one[1][1])
            string_list[y] = string_list[y][:x+1] + ID_string[one[0]] + string_list[y][x+3:]
            string_list[y+1] = string_list[y+1][:x+1] + ID_string[one[0]] + string_list[y+1][x+3:]


        string = "\n".join(string_list)


        print(boundary_top)
        print(string)
        print(boundary_bottom)



    def write_data(self):
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

    def get_world_frame (self, world_i, frame_i):
        world_nframes = [0, 16, 32, 58, 88]
        level_pointer = self.level_pointers[world_nframes[world_i] + frame_i] - 0xCD41
        count = self.table[level_pointer]
        objects = []
        for objec in range(count):
            ID = (self.table[level_pointer+1 + 3*objec])
            objects.append([ID, self.transform_byt_co(
                                    self.transform_small_big(
                                        self.table[level_pointer+2 + 3*objec], 
                                        self.table[level_pointer+3 + 3*objec]))
                            ])

        return objects







    def transform_byt_co(self, big_value):
        assert big_value <= 0x6bc and big_value >=0, "Byte value must be 0 to 0x6BC"
        assert big_value % 2 == 0, "Byte value must be pair, else it will appear gliched."

        y = ( big_value // 0x40) / 2
        x = (big_value % 0x40) / 2
        return x/2, y

    def transform_co_byt(self, x, y):
        assert x <= 15 and x >= 0, "X must be in 0 and 15"
        assert y <= 13 and y >= 0, "Y must b in 0 and 13"
        assert x % 0.5 == 0 and y % 0.5 == 0, "X or Y must be a multiple of 0.5"
        transfo_y = y * 2 * 0x40
        big_value = transfo_y + x * 2 *2
        return int(big_value)

    def transform_small_big(self, low, hi):
        return hi * 16 * 16 + low



    def add_objects(self, world_i, frame_i, object_ids, objects_co):
        assert len(object_ids) == len(objects_co), "Each ID must have it coordinates"
        for one in object_ids:
            assert one in objects.ID.keys(), f"Can't use the id {one}"
        for one in objects_co:
            assert isinstance(one, tuple) and len(one) == 2, "Coordinates must be of (x,y)"

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