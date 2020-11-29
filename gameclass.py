from infos import *
import random
from world import *
from getters import getter_passwords

class RandomizerError(BaseException):
    pass

class ROM:
    header = bytearray(
        [0x47,0x4F,0x4F,0x46,0x20,0x54,0x52,0x4F,0x4F,0x50,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x30,0x00,0x09,0x00,0x01,0x08,0x00,0x2F,0xA5,0xD0,0x5A
        ,0x20,0x50,0x72,0x6F,0xBC,0xFF,0xBC,0xFF,0xBC,0xFF,0xB4,0xFF,0xBC,0xFF,0xB8,0xFF,0x20,0x4D,0x2E,0x20,0xBC,0xFF,0xBC,0xFF,0xBC,0xFF,0xBC,0xFF,0xB0,0xFF,0xBC,0xFF
        ])
    # NOTE for self : it's a LoROM
    # https://en.wikibooks.org/wiki/Super_NES_Programming/SNES_memory_map





    def __init__(self,data):
        """
            First, it checks if it has a header.
            Then it copies the relevant data.
            Then it checks if it's the correct game.
                If not, it will raise an AssertionError
        """
        if len(data) % 1024 == 512:
            self.data = bytearray(data[512:])
        elif len(data) % 1024 == 0:
            self.data = bytearray(data)
        else:
            raise BaseException("Your game seems to be corrupted")
        for n,i in enumerate(self.data[0x7FC0:0x7FFF]):
            assert i == self.header[n]

    def setmulti(self, offset1, offset2, value, jumps=1):
        # The idea of this method is for cases where you need to change the value
        # of a bunch of address that are linked together periodically.
        # I am hoping to make it so that it can use the random module sometimes if this idea is kept.
        for i in range(offset1, offset2 +1, jumps):
            self.data[i] = value


    def __getitem__(self,offset):
        return self.data[offset]
    def __setitem__(self,offset, value):
        self.data[offset] = value

class GT(ROM):
    def __init__(self,data, seed):
        super().__init__(data)  # Header removal
        self.modify_data_ice_dark()  # Changement du code en prévision du randomizer pour pouvoir changer le nombre.
        self.modify_data_starting_frame()  # CHangement du code pour permettre une randomization du first frame. Side effect : Pu d'introduction.
        self.removeExitFromData(3,1,0)  # Enlever exit inutilisé
        self.removeExitFromData(1,15,0) # Enlever exit inutilisé
        self.removeExitFromData(1,13,1) # Enlever exit inutilisé
        self.seed = seed
        self.add_credits()  # Ajout credits



        # Création des différents world pour permettre leur randomization isolé.
        self.all_worlds = [World(self.data, 0),World(self.data, 1),World(self.data, 2),World(self.data, 3),World(self.data, 4)]



    def removeExitFromData(self, world_i, frame_i, index):
        """Remove a specific exit from a said world-frame. 

        Args:
            world_i (int): Which world
            frame ([type]): which frame
            index ([type]): which exit
        """
        offsets, values = [], []
        base = self[0x01F303 + world_i]
        adjust = 0x1F303 + base + 2*frame_i

        #Lecture du Gros Byte. On doit lire le byte présent et le byte suivant et les combiner ensemble.
            # GROS BYTE : 0xHHpp
        temp1 = self[0x1F303 + base + 2*frame_i]  # Cecu est l'endroit où es tle count, du moins les deux premiers bytes on a les deux premiers chiffres! (pp)
        temp2 = self[0x1F303 + base + 2*frame_i + 1]  # Les deux high bytes (HH)
        temp3 = temp2 * 16 * 16 + temp1

        count_offset = 0x10000 + temp3
        vanilla_count = self[count_offset]

        # Preparation for removal
        for i in range(vanilla_count):
            offsets.append(list(count_offset + x + 6 * i + 1 for x in range(6)))
            values.append([self[count_offset + x + 6 * i + 1] for x in range(6)])

        # Actual removal of exit
        if index == vanilla_count -1:  # On pourra ptet enlever les clauses de if/else.
            pass  # Pcq c'était déjà le dernier de la liste.
        else:  # On décale les valeurs.
            for i in range(index, vanilla_count-1):
                for no, offset in enumerate(offsets[i]):
                    self[offset] = values[i+1][no] # Should work
        self[count_offset] -=1


    def modify_data_ice_dark(self):
        """Change old code to new code to be more flexible."""
        self[0x28CC] = 0x64
        self[0x28CD] = 0xCA
        self[0x28CE] = 0xA6
        self[0x28CF] = 0xB6
        self[0x28D0] = 0xA5
        self[0x28D1] = 0xB7
        self[0x28D2] = 0x18
        self[0x28D3] = 0x7F
        self[0x28D4] = 0x30
        self[0x28D5] = 0xFF
        self[0x28D6] = 0x83
        self[0x28D7] = 0xAA
        self[0x28D8] = 0xBF
        self[0x28D9] = 0x30
        self[0x28DA] = 0xFF
        self[0x28DB] = 0x83
        self[0x28DC] = 0x29
        self[0x28DD] = 0x01
        self[0x28DE] = 0xF0
        self[0x28DF] = 0x02
        self[0x28E0] = 0xE6
        self[0x28E1] = 0xCA
        self[0x28E2] = 0x60

        self[0x280E] = 0xBF
        self[0x280F] = 0x30
        self[0x2810] = 0xFF
        self[0x2811] = 0x83
        self[0x2812] = 0x29
        self[0x2813] = 0x02
        self[0x2814] = 0xD0
        self[0x2815] = 0x2822-0x2815

        self.setmulti(0x2816,0x2820, 0xEA)

        # Data table for Ice and Dark rooms
        self[0x1FF30] = 0+5 # World 0
        self[0x1FF31] = 16+5# World 1
        self[0x1FF32] = 32+5# World 2
        self[0x1FF33] = 58+5# World 3
        self[0x1FF34] = 88+5# World4
        self.setmulti(0x1FF35, 0x1FFA6, 0x0)

        dark_rooms_vanilla = [(2,4),(2,20),
                            (3,7),(3,20),
                            (4,15),(4,17)]
        ice_rooms_vanilla = [(3,5),(3,6)]

        for couple in dark_rooms_vanilla:
            self[self.get_darkice_index(couple[0], couple[1])] += 2
        for couple in ice_rooms_vanilla:
            self[self.get_darkice_index(couple[0], couple[1])] += 1

    def modify_data_starting_frame(self):
        """Change the code to allow randomization of first frame.
            Unfortunate effect : Removal of intro cs.
            """


        self[0x1DFD] = 0xA9
        self[0x1DFE] = 0x04
        self[0x1DFF] = 0x85
        self[0x1E00] = 0xA0
        self[0x1E01] = 0xA5
        self[0x1E02] = 0xC3
        self[0x1E03] = 0x85
        self[0x1E04] = 0xB6


        # Jump
        self[0x1E05] = 0x20
        self[0x1E06] = 0x81
        self[0x1E07] = 0xF3
        self[0x1E08] = 0xEA





        # TAX
        self[0x7381] = 0xAA

        # LDA,X
        self[0x7382] = 0xBD
        self[0x7383] = 0xA7  # TO FIX
        self[0x7384] = 0xFF

        # STA B7
        self[0x7385] = 0x85
        self[0x7386] = 0xB7


        #LDA #0
        self[0x7387] = 0xEA#0xA9
        self[0x7388] = 0xEA#0x00

        # LDX #8
        self[0x7389] = 0xA2
        self[0x738A] = 0x8

        #rts
        self[0x738B] = 0x60


        self[0x1F95] = 0xEA
        self[0x1F96] = 0xEA


        #Data
        self[0x1FFA7] = 0   
        self[0x1FFA8] = 0
        self[0x1FFA9] = 0
        self[0x1FFAA] = 0
        self[0x1FFAB] = 0



        # Fix a LDA B7 that should always load 0 and make it a constant instead.
        self[0x2766] = 0xA9
        self[0x2767] = 0x0



        self[0X23E2] = 0x20
        self[0x23E3] = 0x8C
        self[0x23E4] = 0xF3
        self[0x23E5] = 0xEA    
        
        # 80A3E2 INC B6


        self[0x738C] = 0xE6
        self[0x738D] = 0xB6
        self[0x738E] = 0xA6
        self[0x738F] = 0xB6

        # LDA,X
        self[0x7390] = 0xBD
        self[0x7391] = 0xA7  # TO FIX
        self[0x7392] = 0xFF

        # STA B7
        self[0x7393] = 0x85
        self[0x7394] = 0xB7

        self[0x7395] = 0x60



    def darkRandomizer(self, count=6):
        """Randomize which rooms are dark up to the count given (Defaults to vanilla value (6)).
            """
        for offset in range(0x1FF35, 0x1FFA7):  # Remove all dark rooms
            self[offset] = self[offset] & 1
        offsets = [offset for offset in range(0x1FF35, 0x1FFA7)]

        for world, boss_frame in enumerate([14, 15, 25, 25, 25]):
            offsets.pop(offsets.index(self.get_darkice_index(world, boss_frame)))
        random.shuffle(offsets)
        for no in range(count):
            self[offsets[no]] += 2

    def activateWorldSelection(self):
        """Put a banana on the box of the world you want to go.
            Cherry for all the rest of the boxes
            Example : Banana on the 3rd box = World 2 (3rd world of the game)
            """
        self.setmulti(0x1C67F, 0x1C692, 0x0)
        self[0x1c680] = 0x1
        self[0x1c686] = 0x1
        self[0x1c68c] = 0x1
        self[0x1c692] = 0x1

    def iceRandomizer(self, count=2):
        """Randomize which rooms are icy up to the count given (Defaults to vanilla value (2)).
            """
        for offset in range(0x1FF35, 0x1FFA7):  # Remove all ice rooms
            self[offset] = self[offset] & 2
        offsets = [offset for offset in range(0x1FF35, 0x1FFA7)]
        random.shuffle(offsets)
        for no in range(count):
            self[offsets[no]] += 1

    def get_darkice_index(self, world_i,frame_i):
        """Formula to get the indice.
            """
        offsets = [0, 16, 32, 58, 88]
        return offsets[world_i] + frame_i + 0x1FF35

    def add_credits(self):
        """This function will add the credits of the contributors of this project
            in the credits of the game. It defines a function internally, then uses it for each lines.
            """

        def add_credits_line(self, text,*, center=True, color=0, underlined=False, spacing=0xD):
            """ This function will add a single line to the credits of the game.
                """

            assert len(text) <= 32, f"Text line too long ({len(text)}). Must be < 32"
            assert color <= int("1111", base=2), "0 < Color < 0" # FIXME : I tried to check if color < 0, but couldn't make it work.

            credits_range = self[0x5F99E: 0x5FDFF +1]
            offset = credits_range.index(0xFF) + 0x5F99E
                # 0xFF will call the "THE END sprites if it's at "nombre de return"
                # In other words, this will fetch the end of the current credits.
            stats = self[offset: offset +20]
                # After the credits, the total time is there. I need to keep them, so I created
                # a new variable.

            self[offset] = spacing  # Nb de returns (vertical spacing)
            offset += 1
            self[offset] = 16 - len(text) // 2 if center else 1 # Horizontal Alignement
            offset += 1
            self[offset] = len(text)  # nombre de lettres
            offset += 1
            self[offset] = color * 4
                    # bit 0 displayed the text weirdly (jap?)
                    # bit 1 displayed nothing => If set, always display nothing?
                    # bit 2 - 5 : Color stuffs
                    # byte 6-7 : Mirrors stuffs

            for letter in text:  # Writting the string
                offset += 1
                self[offset] = ord(letter.upper())
            for value in stats:
                offset += 1
                assert offset <= 0x5FDFF, "Too much text added"  # This is the check to make sure we don't pass the allowed range.
                self[offset] = value
            if underlined:
                string = "¨" * len(text)
                add_credits_line(self, string ,center=center, color=color, spacing=0x1)

        add_credits_line(self, "Goof Troop randomizer", underlined=True, color=4, spacing=16)
        add_credits_line(self, "Version alpha", spacing=1)
        add_credits_line(self, f"Seed : {self.seed}", spacing=1)
        add_credits_line(self, "Flags used : alpha", spacing=1)
        add_credits_line(self, "Developpers", underlined=True, color=5)
        add_credits_line(self, "Data structure & management", underlined=True, color=5, spacing = 0x4)
        add_credits_line(self, "Guylain Breton - Niamek", spacing=1)
        add_credits_line(self, "Randomization logic & code", underlined=True, color=5, spacing=0x4)
        add_credits_line(self, "Charles Matte-Breton", spacing=1)
        add_credits_line(self, "Special thanks", underlined=True, color=3)
        add_credits_line(self, "PsychoManiac", spacing=2)
        add_credits_line(self, "Zarby89", spacing=2)

    def passwordRandomizer(self):
        """Password randomizer"""
        password = [0x0, 0x1, 0x2, 0x3]

        check = False
        while check is False:
            # Actual randomization of the password
            for i in getter_passwords("all"):
                self[i] = random.choice(password)

            # Let's check if two passwords are identical  
            Worlds_passwords = []
            for world in range(1,5):
                Worlds_passwords.append(list(self.data[offset] for offset in getter_passwords(world)))
            check = all([1 == Worlds_passwords.count(x) for x in Worlds_passwords])


    def randomizerWithVerification(self, options):

        fix_boss_exit = True
        fix_locked_doors = True
        keep_direction = options.Rexits_matchdir
        pair_exits = options.Rexits_pair

        exits_rando = options.Rexits
        items_rando = options.Ritems_pos or options.Ritems
        firstframe_rando = options.Rfirst
        max_iter = 50
        for world_i, this_world in enumerate(self.all_worlds):
            for i in range(max_iter):
                for j in range(max_iter):#exits and items randomization
                    if exits_rando:
                        for k in range(max_iter):
                            this_world.exits.randomize(fix_boss_exit,fix_locked_doors,keep_direction,pair_exits)
                            if this_world.allFramesConnectedVerification(): break
                    find = False
                    for k in range(max_iter):
                        if items_rando:
                            this_world.items.randomize(options.Ritems_pos)
                        if firstframe_rando:
                            this_world.randomizeFirstExit()
                        #check feasability
                        unlocked_exits, unlocked_items, boss_reached, early_boss_indicator = this_world.feasibleWorldVerification()
                        if (all(unlocked_exits) and all(unlocked_items) and boss_reached): find = True
                        if find: break
                    if find: break
                    
                if j<(max_iter-1):
                    print('Found a feasible configuration. Calculating feasibility ratio...')

                    feasibility_results = []#shows how many times we do not get stuck if we play randomly
                    early_boss_results = []
                    for m in range(50):
                        unlocked_exits, unlocked_items, boss_reached, early_boss_indicator = this_world.feasibleWorldVerification()
                        feasibility_results.append((all(unlocked_exits) and all(unlocked_items) and boss_reached))
                        early_boss_results.append(early_boss_indicator)
                    
                    print(sum(feasibility_results)/len(feasibility_results))
                    print(sum(early_boss_results)/len(early_boss_results))
                    if (sum(feasibility_results)/len(feasibility_results))==1 and (sum(early_boss_results)/len(early_boss_results))>0.85: 
                        this_world.writeWorldInData()

                        print('Assigned new exits and items to world',world_i)
                        break
                else: 
                    raise RandomizerError(f"Was not able to find a feasible configuration with these settings for world {world_i}")
