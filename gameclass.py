from world import *

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
        for i in range(offset1, offset2 +1, jumps):
            self.data[i] = value

    def rewrite(self, start, iterable_rewrite):
        for no, byte in enumerate(iterable_rewrite):
            self.data[start + no] = byte


    def __getitem__(self,offset):
        return self.data[offset]
    def __setitem__(self,offset, value):
        self.data[offset] = value

class GT(ROM):
    def __init__(self,data, seed):
        super().__init__(data)  # Header removal
        self.modify_data_ice_dark_alert()  # Changement du code en prévision du randomizer pour pouvoir changer le nombre.
        self.modify_data_stars()
        self.removeExitFromData(3,1,0)  # Enlever exit inutilisé
        self.removeExitFromData(1,15,0) # Enlever exit inutilisé
        self.removeExitFromData(1,13,1) # Enlever exit inutilisé
        self.seed = seed
        self.add_credits()  # Ajout credits

        self.setmulti(0x72A9, 0x72D5, 0xEA)  # Free space from piracy check


        self.setmulti(0x0131DF, 0x131E0, 0xEA)  # Disable the counter so you never see demo
            # I did this because if we happen to have a dark room in demo, the screens will be glitchy


        # Création des différents world pour permettre leur randomization isolé.
        self.all_worlds = [World(self.data, 0),World(self.data, 1),World(self.data, 2),World(self.data, 3),World(self.data, 4)]

    def arrow_platform_bidirect(self):
        self.rewrite(0xDD62, [0x22, 0x33,0xFF,0x81])
        self.rewrite(0xFF33, [0xAD, 0x11, 0x1, 0xC9, 0xC0, 0xB0, 
                                0x5, 0xA9, 0x02, 0x85, 0x02, 0x6B,
                                0xA9, 0xA8, 0x8D, 0x61, 0x02, 0xA9,
                                0x48, 0x8D, 0x64, 0x02, 0xA9, 0x02,
                                0x85, 0x02, 0x6B])


    def removeExitFromData(self, world_i, frame_i, index):
        """Remove a specific exit from a said world-frame. 
                index (int): which exit
           """
        offsets, values = [], []
        base = self[0x01F303 + world_i]

        count_offset = 0x10000 + self[0x1F303 + base + 2*frame_i + 1] * 16 * 16 + self[0x1F303 + base + 2*frame_i]
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
                    self[offset] = values[i+1][no]
        self[count_offset] -=1

    def modify_data_stars(self):
        # Moving the entire table
        values = []
        for offset in range(0x14621,0x14D32):
            values.append(self[offset])
        self.rewrite(0x14D41, values)

        # Fixing the pointers:
        for offset in range(0x01453D, 0x014621, 2):
            try:
                self[offset] += 0x20
                self[offset+1] += 0x7
            except ValueError:
                self[offset] += 0x20 - 256
                self[offset+1] += 0x8
    
        # Moving the kickable stars to the end to ease modifications.
        for world_i in range(5):
            for frame_i in range([16, 16, 26, 30, 26][world_i]):
            # frame_i in range([4, 0, 0, 0, 0][world_i]):
                values_else, values_stars = [], []
                world_pointer = self[0x014538 + world_i]
                level_pointer = self[0x14538 + 1 + world_pointer + 2*frame_i] * (16 * 16) + self[0x14538 + world_pointer + 2*frame_i]
                offset = 0x8000 + level_pointer
                count = self[offset]
                if count !=0:
                    for item in range(count):
                        if self[offset +1 + item*3] == 0x1A:
                            values_stars += [self[offset +1 + item*3], self[offset +2 + item*3], self[offset +3 + item*3]]
                        else:
                            values_else += [self[offset +1 + item*3], self[offset +2 + item*3], self[offset +3 + item*3]]
                    self.rewrite(offset, [count] + values_else + values_stars)


    def fix_misdirection(self):
        self.setmulti(0x27F2, 0x27F4, 0xEA)
        self.setmulti(0x27FF, 0x2801, 0xEA)

    def modify_data_ice_dark_alert(self):
        """Change old code to new code to be more flexible."""
        self.rewrite(0x28CC,
            [0x64, 0xCA, 0xA6, 0xB6, 0xA5, 0xB7, 0x18,
             0x7F, 0x30, 0xFF, 0x83, 0xAA, 0xBF, 0x30,
             0xFF, 0x83, 0x29, 0x01, 0xF0, 0x02, 0xE6,
             0xCA, 0x60])
        """
        self.rewrite(0x280E,
            [0xBF, 0x30, 0xFF, 0x83, 0x29, 0x02, 0xD0,
             0x2822-0x2815])
        self.rewrite(0x2816,
                [0xBF, 0x30, 0xFF, 0x83, 0x29, 0x04, 0xF0, 0x2820-0x281D, 0x8D, 0x4F, 0x1A])
        """
        self.rewrite(0x280E,
                [0xBF, 0x30, 0xFF, 0x83, 0x29, 0x04, 0xF0, 0x2818-0x2815, 0x8D, 0x4F, 0x1A])
        self.rewrite(0x2819,
            [0xBF, 0x30, 0xFF, 0x83, 0x29, 0x02, 0xD0,
             0x2822-0x2820])



        # Building the empty table.
        self.rewrite(0x1FF30, [0+5, 16+5, 32+5, 58+5, 88+5]) # Data offsets for Ice and Dark rooms
        self.setmulti(0x1FF35, 0x1FFA6, 0x0)  # Data table for Ice and Dark.

        # Vanilla values replacement
        for couple in [(2,4),(2,20),(3,7),(3,20),(4,15),(4,17)]:  # Dark rooms vanilla
            self[self.get_darkice_index(couple[0], couple[1])] += 2
        for couple in [(3,5),(3,6)]:  # Ice room vanilla
            self[self.get_darkice_index(couple[0], couple[1])] += 1


    def modify_data_starting_frame(self):
        """Change the code to allow randomization of first frame.
            """
        self.rewrite(0x1F95, [0x20, 0x81, 0xF3, 0xEA])

        self.rewrite(0x7381, 
            [0xA6, 0xB6, 0xBD, 0xA7, 0xFF, 0x85, 0xB7, 
            0x8A, 0x0A, 0xAA,  # ASL B7 for access to table
            0xBD, 0xAC, 0xFF,  # LDA X
            0x8D, 0x4C, 0x01,  # X P1?
            0x8D, 0xCC, 0x01,  # X P2?
            0xBD, 0xAD, 0xFF,  # LDA X
            0x8D, 0x4D, 0x01,  # X P1?
            0x8D, 0xCD, 0x01,  # X P2?
            0x64, 0xA8, 0x60])

        # Building the data table:
        self.setmulti(0x1FFA7, 0x1FFAB, 0)


        self.setmulti(0x1FFAC,0x1FFAC + 9, 0)  # FIXME
            # X0, Y0, X1 , Y1 , X2, Y2, X3, Y3, X4, Y4













        # Jump for when we beat a boss
        self.rewrite(0x23E2,
            [0x20, 0xA0, 0xF3, 0xEA])

        # When we beat a boss
        self.rewrite(0x73A0,  # FIXME : Decaler correctement
            [0xE6, 0xB6, 0xA6, 0xB6,0xBD, 0xA7,
             0xFF, 0x85, 0xB7, 0x60])


    def no_dark(self):
        for offset in range(0x1FF35, 0x1FFA7):  # Remove all dark rooms
            self[offset] = self[offset] & 1

    def no_icy(self):
        for offset in range(0x1FF35, 0x1FFA7):  # Remove all ice rooms
            self[offset] = self[offset] & 2



    def darkRandomizer(self, count=6):
        """Randomize which rooms are dark up to the count given (Defaults to vanilla value (6)).
            """
        for offset in range(0x1FF35, 0x1FFA7):  # Remove all dark rooms
            self[offset] = self[offset] & 5
        offsets = [offset for offset in range(0x1FF35, 0x1FFA7)]

        for world, boss_frame in enumerate([14, 15, 25, 25, 25]):
            offsets.remove(self.get_darkice_index(world, boss_frame))
        offsets.remove(self.get_darkice_index(3,11))  # Cave bell room
        # offsets.remove(self.get_darkice_index(4,19))
        offsets.remove(self.get_darkice_index(4,8))  # That one platform room hulk got
        # offsets.remove(self.get_darkice_index(4,6))

        random.shuffle(offsets)
        for no in range(count):
            self[offsets[no]] |= 2

    def alert_Randomizer(self, count=10):
        """Randomize which rooms are alert up to the count given.
            """
        for offset in range(0x1FF35, 0x1FFA7):  # Remove all alert rooms
            self[offset] = self[offset] & 3
        offsets = [offset for offset in range(0x1FF35, 0x1FFA7)]

        for world, boss_frame in enumerate([14, 15, 25, 25, 25]):
            offsets.remove(self.get_darkice_index(world, boss_frame))
        random.shuffle(offsets)
        for no in range(count):
            self[offsets[no]] |= 4

    def allAlert(self):
        offsets = [offset for offset in range(0x1FF35, 0x1FFA7)]
        for offset in offsets: self[offset] |= 4


    def checksum(self, alldark=False, allice=False, ohko=False):
        """Add some infos on the title screen : checksum for validating races seeds.
            """
        sprites = [
            (0x6, 0x2), (0x8, 0x4), (0xA, 0x4), (0xC, 0x4),
            (0xE, 0x4),(0x28, 0x2),(0x40, 0x6),(0x42, 0x6),
            (0x44, 0x6), (0x46, 0x6),(0x48, 0x6),(0x4A, 0x4), 
            (0x4C, 0x6)]

        self.rewrite(0x0131D4, [0x22,0x20,0xFB,0x8F]) # JSL InputEndLoop
        self.rewrite(0x7FB20, [0xAD, 0x80, 0x00, 0x9, 0x10, 0x8D, 0x80, 0x0])

        current = 0x7FB28
        for no in range(5):  # Drawing the checksum!
            selection = random.choice(sprites)
            self.rewrite(current, [
                0xA9, 0xE0, # LDA X position!
                0x8D, 0xA0 + 4*no, 0x1A,  # STA $1AA0 ;Set X to 0x08
                0xA9, (0x10 + 32*no), # LDA Y position!
                0x8D, 0xA1 + 4*no, 0x1A,  # STA $1AA1 ;Set Y to 0x10
                0xA9, selection[0], # LDA Tile!
                0x8D, 0xA2 + 4*no, 0x1A,  # STA $1AA2 ;Set C (tile) to 0x0C
                0xA9, selection[1], # LDA palette!
                0x8D, 0xA3 + 4*no, 0x1A])  # STA $1AA3 ;Set Palette to 0x04
            current += 20

        self.rewrite(current, [
            0xA9, 0xAA,  # LDA #$AA
            0x8D, 0xA0, 0x1C,# STA $1CA0 ;Set size for the 4 first sprites to 16x16
            0x8D, 0xA1, 0x1C,# STA $1CA0 ;Set size for the 4-8 sprites to 16x16
            # Do more copy if I need more!
            0xC2, 0x20,  # REP #$20 ;Restore Code overwritten by the hook
            0xE6, 0x14,  # INC $14 ;Restore Code overwritten by the hook
            0x6B  # RTL
            ])



    def ohko(self):
        # for touching enemies or thrown projectiles
        self.setmulti(0x5D19, 0x5D1A, 0xEA)
        self.setmulti(0x5D1F, 0x5D20, 0xEA)

        # This works for kicked stones
        self.rewrite(0x54E8, [0x9E, 0x1D, 0x01,0x9E, 0x3F, 0x01,0x80, 0x2])
        # For bombs
        self.rewrite(0x5793, [0x9E, 0x1D, 0x01, 0x9E, 0x3F, 0x01, 0x80, 0x1])
        # For flames
        self.rewrite(0x5D45,[0x64, 0x1D,0x64, 0x3F,0x80, 0xD6])
        # For those fireballs...
        self.rewrite(0x5D75, [0x64, 0x1D, 0x64, 0x3F, 0x80, 0xA6])
        # And for pete hookshot that somehow use a different
        #  code than simply touching him without his hookshot
        self.rewrite(0xD63C, [0x9E, 0x1D, 0x01, 0x9E, 0x3F, 0x01,0x80, 0x2])


    def credits_frames_randomizer(self):
        def credits_cs_offsets(which):
            assert 0 <= which <= 13, f'which must be in range 0-13'
            return 0x0186CD + which * 0xC, 0x0186CD + which * 0xC + 1

        # Add a jump for lifes hacks during credits
        self.rewrite(0x257D, [0x22, 0xB0, 0xFF, 0x8F])
        # Add live hacks during credits
        self.rewrite(0x7FFB0,[
            0xA9, 0xFF, # LDA #FF
            0x8D, 0x57, 0x01, # STA P1
            0x8D, 0xD7, 0x01, # STA P2
            0xA9, 0x02, # LDA #02
            0xA6, 0xB2, # LDX B2
            0x6B] # RTL
            )

        for cs in range(14):
            self[credits_cs_offsets(cs)[0]] = random.randint(0,4)
            self[credits_cs_offsets(cs)[1]] = random.randint(0,[15, 15, 25, 29, 25][self[credits_cs_offsets(cs)[0]]])



    def allDark(self, sanity=True):
        offsets = [offset for offset in range(0x1FF35, 0x1FFA7)]
        
        for world, boss_frame in enumerate([14, 15, 25, 25, 25]):
            offsets.remove(self.get_darkice_index(world, boss_frame))

        for offset in offsets: self[offset] |= 2

    def allIcy(self):
        offsets = [offset for offset in range(0x1FF35, 0x1FFA7)]

        for offset in offsets: self[offset] |= 1


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
            self[offset] = self[offset] & 6
        offsets = [offset for offset in range(0x1FF35, 0x1FFA7)]
        random.shuffle(offsets)
        for no in range(count):
            self[offsets[no]] |= 1

    def get_darkice_index(self, world_i,frame_i):
        """Formula to get the indice.
            """
        offsets = [0, 16, 32, 58, 88]
        return offsets[world_i] + frame_i + 0x1FF35

    def add_credits(self):
        """This function will add the credits of the contributors of this project.
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

            for letter in text:  # Writing the string
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
        add_credits_line(self, "Version 2.0", spacing=1)
        add_credits_line(self, f"Seed : {self.seed}", spacing=1)
        add_credits_line(self, "Developers", underlined=True, color=4)
        add_credits_line(self, "Data structure & management", underlined=True, color=3, spacing = 0x4)
        add_credits_line(self, "Guylain Breton - Niamek", spacing=1)
        add_credits_line(self, "Randomization logic & code", underlined=True, color=2, spacing=0x4)
        add_credits_line(self, "Charles Matte-Breton", spacing=1)
        add_credits_line(self, "Special thanks", underlined=True, color=3)
        add_credits_line(self, "PsychoManiac", spacing=2)
        add_credits_line(self, "Zarby89", spacing=2)

    def getter_passwords(self,world=None):
        """Return the offsets of all passwords
            """
        if world == None:
            return list(range(0x1C67F, 0x1C693))
        return [x for x in range(0x1C67F + 5*(world -1), 0x1C684 + 5*(world-1))]

    def passwordRandomizer(self):
        """Password randomizer"""
        password = [0x0, 0x1, 0x2, 0x3]

        check = False
        while check is False:
            # Actual randomization of the password
            for i in self.getter_passwords():
                self[i] = random.choice(password)

            # Let's check if two passwords are identical  
            Worlds_passwords = []
            for world in range(1,5):
                Worlds_passwords.append(list(self.data[offset] for offset in self.getter_passwords(world)))
            check = all([1 == Worlds_passwords.count(x) for x in Worlds_passwords])

    def randomizerWithVerification(self, options):

        fix_boss_exit = True
        fix_locked_doors = True
        keep_direction = options.Rexits_matchdir
        pair_exits = options.Rexits_pair

        exits_rando = options.Rexits
        items_rando = options.Ritems_pos or options.Ritems
        firstframe_rando = options.Rfirst
        max_iter_big_step = 50000
        max_iter_small_step = 50
        for world_i, this_world in enumerate(self.all_worlds):
            number_of_tries = 0
            print('Trying to find a world configuration for which you cannot get stuck...')
            for i in range(max_iter_big_step):
                for j in range(max_iter_small_step):#exits and items randomization
                    if exits_rando:
                        for k in range(max_iter_small_step):
                            this_world.exits.randomize(fix_boss_exit,fix_locked_doors,keep_direction,pair_exits)
                            if this_world.allFramesConnectedVerification(): break

                    find = False
                    for k in range(max_iter_small_step):
                        if items_rando:
                            this_world.items.randomize(options.Ritems_pos)
                        if firstframe_rando:
                            # this_world.randomizeFirstExit()
                            this_world.randomizeFirstExit()

                        #check feasability
                        unlocked_exits, unlocked_items, boss_reached, early_boss_indicator = this_world.feasibleWorldVerification()
                        number_of_tries += 1
                        if (all(unlocked_exits) and all(unlocked_items) and boss_reached): find = True
                        if find: break
                    if find: break
                    elif number_of_tries>max_iter_big_step:
                        print(f"Was not able to find a feasible configuration with these settings for world {world_i+1}")
                        raise RandomizerError(f"Was not able to find a feasible configuration with these settings for world {world_i+1}")


                if i<(max_iter_big_step-1):
                    feasibility_results = []#shows how many times we do not get stuck if we play randomly
                    early_boss_results = []
                    for m in range(50):
                        unlocked_exits, unlocked_items, boss_reached, early_boss_indicator = this_world.feasibleWorldVerification()
                        feasibility_results.append((all(unlocked_exits) and all(unlocked_items) and boss_reached))
                        if not pair_exits: early_boss_indicator = 1 #the check to make sure that a level is not too quick to finish is removed when exits are not paired
                        early_boss_results.append(early_boss_indicator)
                    
                    #print(sum(feasibility_results)/len(feasibility_results))
                    #print(sum(early_boss_results)/len(early_boss_results))
                    if (sum(feasibility_results)/len(feasibility_results))==1 and (sum(early_boss_results)/len(early_boss_results))>0.85: 
                        
                        if world_i == 4:
                            feasibility_results = []#shows how many times we do not get stuck if we play randomly
                            early_boss_results = []
                            true_starting_exit = deepcopy(this_world.starting_exit)
                            this_world.starting_exit = 36 #room with arrow platform where you can get stuck
                            for m in range(50):
                                unlocked_exits, unlocked_items, boss_reached, early_boss_indicator = this_world.feasibleWorldVerification()
                                feasibility_results.append(boss_reached)
                                early_boss_results.append(early_boss_indicator)
                            this_world.starting_exit = true_starting_exit
                            if (sum(feasibility_results)/len(feasibility_results))==1:
                                this_world.writeWorldInData()
                                print(f"Assigned new exits and items to world {world_i+1} after {number_of_tries} iterations")  # print world number as 1-indexed for readability
                                break

                        elif world_i == 3:
                            feasibility_results = []#shows how many times we do not get stuck if we play randomly
                            early_boss_results = []
                            true_starting_exit = deepcopy(this_world.starting_exit)
                            this_world.starting_exit = 0 #room with door that requires to do a puzzle
                            for m in range(50):
                                unlocked_exits, unlocked_items, boss_reached, early_boss_indicator = this_world.feasibleWorldVerification()
                                feasibility_results.append(boss_reached)
                                early_boss_results.append(early_boss_indicator)
                            this_world.starting_exit = true_starting_exit

                            if (sum(feasibility_results)/len(feasibility_results))==1:
                                this_world.writeWorldInData()
                                print(f"Assigned new exits and items to world {world_i+1} after {number_of_tries} iterations")  # print world number as 1-indexed for readability
                                break
                            
                        else:
                            this_world.writeWorldInData()
                            print(f"Assigned new exits and items to world {world_i+1} after {number_of_tries} iterations")  # print world number as 1-indexed for readability
                            break
                else: 
                    print(f"Was not able to find a feasible configuration with these settings for world {world_i+1}")
                    raise RandomizerError(f"Was not able to find a feasible configuration with these settings for world {world_i+1}")  # print world number as 1-indexed for readability
