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
            ,
            [  # World 2
                (   [0x8, 0x8, 0x8],
                    [(0.5, 11), (1.5, 11), (1.5, 12)]),  # 2-0
                (   [],
                    []),  # 2-1
                (   [0x8 for _ in range(6)],
                    [(2,2), (1, 3), (13,2), (14, 3), (13,12), (14,11)]),
                ([],[]),  # 2-3
                ([],[]),  # 2-4
                (   [0x8 for _ in range(6)],
                    [(1,2), (14,2), (6.5, 7), (8.5, 7), (1, 12), (14,12)]),  # 2-5
                (   [0x2 for _ in range(6)],
                    [(1, 11),(1,12),(2,12),(13,12),(14,12),(14,11)]),  # 2-6
                ([],[]),
                (   [0x2 for _ in range(5)],
                    [(1,2), (1,12), (5, 2), (11, 12), (14, 12)]),  # 2-8
                ([],[]),  # 2-9
                (   [0x2, 0x2, 0x2, 0x1A, 0x1A, 0x1A, 0x1A],
                    [(1, 2), (1, 12), (14, 6), (2, 6), (8, 5), (8, 7), (10, 6)]),  # 2-10
                ([],[]),  # 2-11
                (   [0x2 for _ in range(7)],
                    [(3, 3.5), (7, 3.5), (11, 3.5), (4.5, 8.5), (5.5, 8.5), (8.5, 8.5), (9.5, 8.5)]),  # 2-12
                ([],[]),  # 2-13
                (   [0x2 for _ in range(8)],
                    [(1, 6), (1, 7), (1, 8), (1, 12), (10, 2), (9,5), (10, 5), (14, 12)]),  # 2-14
                ([],[]),  # 2-15
                (   [0x2 for _ in range(4)],
                    [(1, 2), (6, 6), (9, 6), (14, 2)]),  # 2-16
                (   [0x0 for _ in range(8)],
                    [(1, 2), (1, 3), (2, 3), (1,12), (6, 7.5), (6, 8.5), (10, 8.5), (14, 2)]),  #2-17
                (   [0x2 for _ in range(4)],
                    [(1, 2), (2, 2), (13, 2), (14, 2)]),  # 2-18
                (   [0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x20, 0x20],
                    [(11, 5), (4, 7.5), (5, 7.5), (4, 10), (5, 10), (13, 9), (12, 9), (12, 12)]),  # 2-19
                (   [0X2, 0X2, 0X2],
                    [(2, 5), (1, 12), (14, 12)]),  # 2-20
                (   [0x2 for _ in range(6)],
                    [(2, 7), (2, 8), (2, 9), (5, 9), (6, 9), (14,11)]),  # 2-21
                ([],[]),  # 2-22
                ([0x20, 0x20, 0x2, 0x2, 0x2, 0x2, 0x2],[(12, 2), (12, 3), (2,2), (2,3), (4, 5.5), (4, 7.5), (9, 11)]),  # 2-23
                ([],[]),  # 2-24
                ([],[])  # 2-25
                ]
            ,
            [  # World 3
                (   [0x0 for _ in range(6)],
                    [(1, 5), (2, 5), (3, 5), (12,5), (13,5), (14,5)]),  # 3-0
                (   [0x20, 0x20, 0x20, 0x20, 0x0, 0x0],
                    [(6,8), (7,8), (8,8), (10,6), (7,7), (8,7)]),  # 3-1
                (   [0x0 for _ in range(14)],
                    [(12, 2), (12, 3), (13,3), (14,3), (14,2), 
                        (10, 7), (11, 7), (12, 7), (13, 7), 
                        (12,11), (12, 12), (13,11), (14,11), (14,12)]),  # 3-2
                ([0x0 for _ in range(14)],
                    [(1,6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), 
                        (7,2), (7,3), (8,2), (8,3), 
                        (9,5), (10,5), 
                        (13,5), (14,5)]),  # 3-3
                (   [0x20, 0x1E, 0x1E ],
                    [(8.5, 7), (4,4), (5,10)]),  # 3-4
                ([],[]),  # 3-5
                (   [0x0 for _ in range(6)],
                    [(3,8), (6.5, 5.5), (6.5, 7), (8.5, 5.5), (8.5, 7), (12,6)]),  #3-6
                ([],[]),  # 3-7
                (   [0x0 for _ in range(16)],
                    [(7,3), (7,4), (7,5), (7,6),
                        (8,3), (8,4), (8,5), (8,6),
                        (7,8), (7,9), (7,10), (7,11),
                        (8,8), (8,9), (8,10), (8,11),
                        ]),  # 3-8
                (   [0x1E, 0x1E, 0x1E, 0x1E, 0x20],
                    [(1, 6), (1, 8), (1, 10), (3, 5)]),  # 3-9
                (   [0x1A for _ in range(7)],
                    [(2, 10), (4, 4), (7, 5), (6, 10), (10, 9), (12, 12), (13, 4)]),  #3-10
                (   [0x1A, 0x1A],
                    [(5, 10), (10, 10)]),  # 3-11
                ([],[]),  # 3-12
                (   [0x0 for _ in range(13)],
                    [(1,2), (1,3), (2,3), (4,3), (4,2),
                    (1, 12), (2, 12),
                    (9,8), (10, 8),
                    (14,2), (14,3)]),  # 3-13
                (   [0x0, 0x1A, 0x1A, 0x1A, 0x1E, 0x1E, 0x1C, 0x1C],
                    [(7, 8),
                    (4, 3), (5, 4), (10, 8),
                    (11, 5), (1, 8),
                    (6, 9), (7, 4)
                    ]),  # 3-14
                ([],[]),  # 3-15
                (   [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1A, 0x1A, 0x1C, 0x1C, 0x1C, 0x1C],
                    [(5, 9), (6, 9), (7, 8), (8, 8), (9, 9), (10, 9),
                    (2, 5),
                    (12, 5), (13, 5),
                    (3, 7), (13, 6),
                    (3, 8), (5, 10), (8, 10), (10, 8)
                    ]),  # 3-16
                (   [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1C, 0x20],
                    [(1, 7), (2, 9), (1, 11), (2, 12),
                    (8, 12),
                    (14, 9), (14, 10), (14, 11), (14, 12),
                    (9.5, 5), (8, 11)]),  # 3-17
                ([],[]),  # 3-18
                ([],[]),  # 3-19
                (   [0x1A, 0x1A, 0x1A, 0x1A, 0x1A],
                    [(2, 9), (2, 5), (4, 5), (10, 5), (12, 8), ]),  # 3-20
                (   [0x1A, 0x1A, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C],
                    [(7, 7), (8, 7),
                    (4, 4), (2, 5),
                    (11, 4), (12, 5),
                    (6, 10), (9, 10)]),  # 3-21
                ([],[]),  # 3-22
                ([0x1A, 0x1C, 0x1C],
                    [(6, 6), (7, 6), (3, 5)]),  # 3-23
                ([0x0 for _ in range(12)],
                [(1, 11), (2, 11), (1, 12), (2, 12), (3, 12), (4, 12),
                (13, 11), (14, 11), (11, 12), (12, 12), (13, 12), (14, 12)]),  #3-24
                ([],[]),  # 3-25
                (   [0x0 for _ in range(14)],
                    [(12, 2), (12, 3), (13,3), (14,3), (14,2), 
                        (10, 7), (11, 7), (12, 7), (13, 7), 
                        (12,11), (12, 12), (13,11), (14,11), (14,12)]),  # 3-26
                ([0x0 for _ in range(14)],
                    [(1,6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), 
                        (7,2), (7,3), (8,2), (8,3), 
                        (9,5), (10,5), 
                        (13,5), (14,5)]),  # 3-27
                (   [0x0 for _ in range(16)],
                    [(7,3), (7,4), (7,5), (7,6),
                        (8,3), (8,4), (8,5), (8,6),
                        (7,8), (7,9), (7,10), (7,11),
                        (8,8), (8,9), (8,10), (8,11),
                        ]),  # 3-28
                (   [0x0 for _ in range(16)],
                    [(7,3), (7,4), (7,5), (7,6),
                        (8,3), (8,4), (8,5), (8,6),
                        (7,8), (7,9), (7,10), (7,11),
                        (8,8), (8,9), (8,10), (8,11),
                        ])  # 3-29
                ]
            ,
            [  # World 4
                (   [0x0 for _ in range(6)],
                    [(11, 11), (12, 11), (13, 11), (11, 12), (12, 12), (13, 12)]),  # 4-0
                (   [0x0 for _ in range(11)],
                    [   (3, 10),
                        (1, 8), (1, 5),
                        (5, 2),
                        (4, 8),
                        (7, 10), (8, 12),
                        (11, 2), (11, 3),
                        (13, 2), (14, 2)]),  # 4-1
                ([0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1A, 0x1A, 0x1A],
                    [(1, 6), (1, 7),
                    (6, 12), (7, 12),
                    (13, 10), (14, 10), (11, 11), (11, 12),
                    (3, 10), (2, 11), (1, 12)]),  # 4-2
                (   [0x1A for _ in range(7)],
                    [(8, 4), 
                    (5, 7), (6, 7), (8, 7),
                    (3, 12), (7, 12),
                    (14, 5)]),  # 4-3
                ([],[]),  # 4-4
                ([0x1C],[(7, 11)]),  # 4-5
                ([],[]),  # 4-6
                ([0x2 for _ in range(8)],
                    [(1, 2), (4, 2),
                    (11, 2), (14, 2),
                    (1, 12), (4, 12),
                    (11, 12), (14, 12)]),  # 4-7
                ([0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1A, 0x1A],
                    [(1, 2), (1, 3), (1, 4), (1, 5),
                    (1, 9), (1, 10), (1, 11), (1, 12),
                    (11, 2), (11, 3),
                    (7, 11), (7, 12)]),  # 4-8
                ([0x0 for _ in range(6)],
                [(12, 2), (13, 2), (14, 2),
                (12, 3), (13, 3), (14, 3)]),  # 4-9
                ([0x1A, 0x1A],[(5, 7), (7, 5)]),  # 4-10
                (   [0x0 for _ in range(4)],
                    [(1, 11), (2, 11), 
                    (13, 11), (14, 11)]),  # 4-11
                (   [0x1A, 0x1A, 0x1A, 0x1A, 0x1A],
                    [(7, 4), (10, 4), 
                    (8, 7), 
                    (4, 10), (7, 10)]),  # 4-12
                ([],[]),  # 4-13
                (   [0x20, 0x20, 0x20, 0x20, 0x1E, 0x1E, 0x1C, 0x1C],
                    [(4, 6), (5, 6),
                    (10, 6), (11, 6),
                    (7, 10),(8, 10),
                    (13, 8), (2, 8)]),# 4-14
                
                
                ([0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                    [
                        (9, 12), 
                        (5, 6),(7, 6),
                        (2, 3), (1, 4),
                        (2, 11),
                        (8, 9),
                        (11, 12), (13, 10)
                        (8, 4)
                        (13, 3), (12, 3), (11, 3)
                        ]),  # 4-15
                (   [0x0, 0x0, 0x0],
                    [(6, 9), (7, 9), (8, 9)]),  # 4-16
                ([0x0, 0x0, 0x0, 0x0, 0x0, 0x1A, 0x1A],
                    [   (10, 12), (11, 12),
                        (14, 9),(13, 9),
                        (5, 9),
                        (8, 8), (11, 5)
                        ]),  # 4-17
                ([],[]),  # 4-18
                ([],[]),  # 4-19
                ([0x0 for _ in range(4)],
                [(1, 3), (1, 2),
                (6, 6), (6, 7)]),  # 4-20
                ([],[]),  # 4-21
                ([0x1A for _ in range(4)],
                    [(5, 7),
                    (7, 8), (7, 8),
                    (10, 7)]),  # 4-22

                (   [0x1A, 0x0, 0x0, 0x0,0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                    [
                        (3,7),
                        (4,5), (5,5), (6,5), (7,5),
                        (4,6), (5,6), (6,6), (7,6), (8, 6),
                        (4, 7), (5, 7), (7, 7), (8, 7),
                        (4, 8), (5, 8), (6, 8), (7, 8), (8, 8),
                        (4, 9), (5, 9), (6, 9), (7, 9)
                        ]),  # 4-23
                ([],[]),  # 4-24
                ([],[])  # 4-25
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