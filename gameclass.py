from patch import *
from world import *


def get_world_indexs(world=None):
    if not world:
        assert 0 <= world <= 4, "World must be 0, 1, 2, 3 or 4"
        id_per_world =   [0, 16, 32, 58, 88, 114]
        return range(id_per_world[world], id_per_world[world+1])
    else:
        return range(114)


def room_to_index(tup=None, id=None):
        id_per_world =   [0, 16, 32, 58, 88]
        if tup:
            return id_per_world[tup[0]] + tup[1]
        if id:
            for world, borne in enumerate(id_per_world[-1::-1]):
                if id >= borne:
                    return (4 - world, id - borne)
        if id == 0:
            return (0,0)


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
    def __init__(self, data):
        super().__init__(data)  # Header removal
        file_size = len(self.data)
        num_bytes = file_size
        num_banks = int(num_bytes / 32768)

        # Cast rom_data to array of c_ubyte to pass to the DLL (don't copy)
        bytes = (c_ubyte * len(rom_data)).from_buffer(rom_data)


        # Unused regions of the original ROM the DLL can use to put data and code into
        holes_list = [
            # unused
            s_rom_hole(  0x7380,  0xC20 ),
            s_rom_hole(  0xFF40,   0xB0 ),
            s_rom_hole( 0x14D50, 0x10A0 ),
            s_rom_hole( 0x1FAF0,  0x500 ),
            s_rom_hole( 0x2A7A0, 0x1850 ),
            s_rom_hole( 0x47E10,  0x1E0 ),
            s_rom_hole( 0x4FD60,  0x290 ),
            s_rom_hole( 0x5E250,  0x5A0 ),
            s_rom_hole( 0x5FBF0,  0x200 ),
            s_rom_hole( 0x7B5D0, 0x1E20 ),
            s_rom_hole( 0x7FB30,  0x2C0 ),
            # gtiles, ctiles & exits
            s_rom_hole( 0x18CE7, 0x00E9 ), # addr [$838CE7, $838DD0)
            s_rom_hole( 0x1F303, 0x06BF ), # addr [$83F303, $83F9C2)
            s_rom_hole( 0x48000, 0x5280 ), # addr [$898000, $89D280)
            s_rom_hole( 0x4F100, 0x0C48 ), # addr [$89F100, $89FD48)
            s_rom_hole( 0x50000, 0x3F70 ), # addr [$8A8000, $8ABF70)
            s_rom_hole( 0x54000, 0x1FB8 ), # addr [$8AC000, $8ADFB8)
            s_rom_hole( 0x58000, 0x6240 ), # addr [$8B8000, $8BE240)
            # itile data
            s_rom_hole( 0x14538,  0x7FA ), # addr [$82C538, $82CD32)
            # class 1 & 2 sprite data
            s_rom_hole(  0x6760,  0xB49 )] # addr [$80E760, $80F2A9)

        num_holes = len(holes_list)
        # Cast holes_list to array of s_rom_hole to pass to the DLL (don't copy)
        holes = (s_rom_hole * num_holes)(*holes_list)

        # Return 1 on success, 0 on error
        self.data = lib.commence(num_banks, pointer(bytes), num_holes, pointer(holes))

    def arrow_platform_bidirect(self):
        self.rewrite(0xDD62, [0x22, 0x33,0xFF,0x81])
        self.rewrite(0xFF33, [0xAD, 0x11, 0x1, 0xC9, 0xC0, 0xB0, 
                                0x5, 0xA9, 0x02, 0x85, 0x02, 0x6B,
                                0xA9, 0xA8, 0x8D, 0x61, 0x02, 0xA9,
                                0x48, 0x8D, 0x64, 0x02, 0xA9, 0x02,
                                0x85, 0x02, 0x6B])

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
                for j in range(max_iter_big_step):#exits and items randomization
                    if exits_rando:
                        for k in range(max_iter_big_step):
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


                if i<(max_iter_big_step-1) and find:
                    feasibility_results = []#shows how many times we do not get stuck if we play randomly
                    early_boss_results = []
                    for m in range(50):
                        unlocked_exits, unlocked_items, boss_reached, early_boss_indicator = this_world.feasibleWorldVerification()
                        feasibility_results.append(boss_reached)
                        if not pair_exits: early_boss_indicator = 1 #the check to make sure that a level is not too quick to finish is removed when exits are not paired
                        early_boss_results.append(early_boss_indicator)
                    
                    #print(sum(feasibility_results)/len(feasibility_results))
                    #print(sum(early_boss_results)/len(early_boss_results))
                    if (sum(feasibility_results)/len(feasibility_results))==1 and (sum(early_boss_results)/len(early_boss_results))>0.85: 

                        if world_i == 3:
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
                            
                        # elif world_i == 4:
                        #     feasibility_results = []#shows how many times we do not get stuck if we play randomly
                        #     early_boss_results = []
                        #     true_starting_exit = deepcopy(this_world.starting_exit)
                        #     this_world.starting_exit = 36 #room with arrow platform where you can get stuck
                        #     for m in range(50):
                        #         unlocked_exits, unlocked_items, boss_reached, early_boss_indicator = this_world.feasibleWorldVerification()
                        #         feasibility_results.append(boss_reached)
                        #         early_boss_results.append(early_boss_indicator)
                        #     this_world.starting_exit = true_starting_exit
                        #     if (sum(feasibility_results)/len(feasibility_results))==1:
                        #         this_world.writeWorldInData()
                        #         print(f"Assigned new exits and items to world {world_i+1} after {number_of_tries} iterations")  # print world number as 1-indexed for readability
                        #         break

                        else:
                            this_world.writeWorldInData()
                            print(f"Assigned new exits and items to world {world_i+1} after {number_of_tries} iterations")  # print world number as 1-indexed for readability
                            break
                else: 
                    print(f"Was not able to find a feasible configuration with these settings for world {world_i+1}")
                    raise RandomizerError(f"Was not able to find a feasible configuration with these settings for world {world_i+1}")  # print world number as 1-indexed for readability



if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as game:
        test = GT(game.read())