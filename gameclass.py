from patch import *
from objects import Versions, Grabbables
from generic import world_indexes, room_to_index, RandomizerError
from world import World2

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
            raise RandomizerError("Your game seems to be corrupted")
        for n,i in enumerate(self.data[0x7FC0:0x7FFF]):
            assert i == self.header[n]

class GT(ROM):
    def __init__(self, data):
        super().__init__(data)  # For header removal, Will be gone eventually once the patch can handle this.


        # Code from psychomaniac, converted to class attributes.
        # Unused regions of the original ROM the DLL can use to put data and code into
        holes_list = [  # All the free space we have TODO : Compare with my findings
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

        self.lib = cdll.LoadLibrary('./patch.dll')
        self.lib.commence.restype = POINTER(s_rom_data)
        self.lib.conclude.restype = c_uint

        # The DLL expects a buffer exactly 2 MiB in size (maximum size of a LoROM)
        rom_data = bytearray(2<<20)


        # Cast rom_data to array of c_ubyte to pass to the DLL (don't copy)
        bytes = (c_ubyte * len(self.data)).from_buffer(self.data)


        num_banks = int(len(self.data) / 0x80000)
        holes = (s_rom_hole * len(holes_list))(*holes_list)


        # This is our complete game data.
        self.data_complete = self.lib.commence(num_banks, pointer(bytes), len(holes_list), pointer(holes))

        # End of Psychomaniac's code importation.

        
        # This is the workable data  (WIP, need to generate a debug file to test)
        self.data = self.data_complete.contents.game
        #self.Versions = Versions(self.data)
        #self.Grabbables = Grabbables(self.data)
        #self.Worlds = [World2(self.data, x) for x in range(5)]



    def __str__(self):
        def get_dark_rooms():
            dark_rooms = []
            for id in world_indexes():
                if self.data.screens[id].flags & 2:
                    dark_rooms.append(str(room_to_index(id=id)))
            return f'{len(dark_rooms)} Dark Rooms: ' + " ".join(dark_rooms)
        def get_ice_rooms():
            ice_rooms = []
            for id in world_indexes():
                if self.data.screens[id].flags & 1:
                    ice_rooms.append(str(room_to_index(id=id)))
            return f'{len(ice_rooms)} Icy Rooms: ' + " ".join(ice_rooms)
        line = "\n" + "-" * 50 + "\n"
        return f'{get_dark_rooms()}\n{get_ice_rooms()}'


    def arrow_platform_bidirect(self):
        self.rewrite(0xDD62, [0x22, 0x33,0xFF,0x81])
        self.rewrite(0xFF33, [0xAD, 0x11, 0x1, 0xC9, 0xC0, 0xB0, 
                                0x5, 0xA9, 0x02, 0x85, 0x02, 0x6B,
                                0xA9, 0xA8, 0x8D, 0x61, 0x02, 0xA9,
                                0x48, 0x8D, 0x64, 0x02, 0xA9, 0x02,
                                0x85, 0x02, 0x6B])


    """
        def checksum(self, alldark=False, allice=False, ohko=False):
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
    """

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

"""
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

"""

if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as game:
        test = GT(game.read())

        test.Versions()