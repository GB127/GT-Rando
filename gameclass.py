from infos import *
import random
from world import *
from getters import getter_passwords

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
    def change_ice_dark_code(self):
        """Change old code to new code to be more flexible.

            Will reduce number of lines eventually.
        """
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


        # Data for Ice and Dark rooms
        self[0x1FF30] = 0+5 # World 0  Ceci c'est bon
        self[0x1FF31] = 16+5# World 1  Ceci c'est bon
        self[0x1FF32] = 33+5# World 2
        self[0x1FF33] = 58+5# World 3
        self[0x1FF34] = 84+5# World4
        self.setmulti(0x1FF35, 0x1FF35 + (84+25), 0x0)


    def __init__(self,data):
        super().__init__(data)
        self.change_ice_dark_code()

    def add_credits(self):
        """
            This function will add the credits of the contributors of this project
            in the credits of the game. It defines a function internally, then uses it for each lines.
        """

        def add_credits_line(self, text,*, center=True, color=0, underlined=False, spacing=0xD):
            """ This function will add a single line to the credits of the game.

            Args:
                text (str) : The text to be written. Max 32 characters as it's the width of the screen.
                center (bool, optional): Centered text or not. Defaults to True.
                color (int, optional): Color, must be 0-15 currently. Defaults to 0 (white).
                underlined (bool, optional): Will underline the words. Defaults to False.
                spacing (int, optional): Vertical spacing. Defaults to 0xD.
            """

            assert len(text) <= 32, f"Text line too long ({len(text)}). Must be < 32"
            assert color <= int("1111", base=2), "0 < Color < 0" # FIXME : I tried to check if color < 0, but couldn't make it work.

            credits_range = self[0x5F99E: 0x5FFFF +1]  
                # This is the entire range available for writting the credits... Almost. 
                # I did not make sure it won't scrap the palettes that are stored futher in the region.
                # Eventually I'll try to fix that. But it seems daunting and tedious... And I'm tired to watch the credits :P
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
                    # byte 0 displayed the text weirdly (jap?)
                    # byte 1 displayed nothing => If set, always display nothing?
                    # byte 6-7 : Mirrors stuffs
                    # All the others are colors stuffs

                    # By multiplying by 4, we are doing two shift left and 
                    # then dodge the bits 0 and bits 1 being set.
                    # Since we can't have bits 6 and 7 set as well, we then cannot
                    # have an initial color higher than 15 (in binary : 1111).
            for letter in text:  # Writting the string
                offset += 1
                self[offset] = ord(letter.upper())
            for value in stats:
                offset += 1
                assert offset <= 0x5FFFF, "Too much text added"  # This is the check to make sure we don't pass the allowed range.
                    # Currently, we can write up to the end of the bank, overwritting the palettes section.
                self[offset] = value
            if underlined:
                # An underline is simply a new line with "¨".
                string = "¨" * len(text)
                add_credits_line(self, string ,center=center, color=color, spacing=0x1)

        add_credits_line(self, "Goof Troop randomizer", underlined=True, color=4)
        add_credits_line(self, "Version alpha", spacing=1)
        add_credits_line(self, "Flags used : alpha", spacing=1)
        add_credits_line(self, "Developpers", underlined=True, color=5)
        add_credits_line(self, "GB127 - Niamek", spacing=2)
        add_credits_line(self, "Charles342", spacing=2)
        add_credits_line(self, "Special thanks", underlined=True, color=3)
        add_credits_line(self, "PsychoManiac", spacing=2)

    def password_randomizer(self):  # Note : I have made a function that will simplify this a lot.
        """
            This is the password shuffler, to make sure one doesn't cheat.

            All password are shuffled and could be anything. There is also a check to make sure
            That all worlds can be accessed (IE no 2 passwords are identical).


            Summary :
                randomize each box seperately
                check if each set of 5 are the same (one world is 5 boxes)
        """
        password = [0x0, 0x1, 0x2, 0x3]

        check = False
        while check is False:
            # Actual randomization of the password
            for i in getter_passwords("all"):
                self[i] = random.choice(password)

            # Let's check if two passwords are identical  
            # FIXME : I'm pretty sure it's possible to combine these five 
            # following lines into a single line. Not sure how to though.
            World_1_pass = list(self.data[offset] for offset in getter_passwords(1))
            World_2_pass = list(self.data[offset] for offset in getter_passwords(2))
            World_3_pass = list(self.data[offset] for offset in getter_passwords(3))
            World_4_pass = list(self.data[offset] for offset in getter_passwords(4))

            Worlds_passwords = [World_1_pass, World_2_pass, World_3_pass, World_4_pass]
            check = all([1 == Worlds_passwords.count(x) for x in Worlds_passwords])

    def darkrooms_randomizer(self):
        """
            This is a dark room randomizer : It randomizes what rooms can be dark!
            Currently there is NO logic. Any world can have any number of rooms
            (I've seen 4 dark rooms in world 1 for example)

            FIXME : Make sure *all rooms can be randomized.
                We need to replace 3 by the highest number a world have. And make sure the boss room isn't in the range

            I've tried a darkroom in a boss room. It almost works. There is probably something that we have to disable
            to make it work for bosses.
                On world 0 boss for example, we see the darkness, then you see the level over everything. 
                The game still works, so it's not a softlock or crash. You just don't see anything.

            I'd like to have this randomizer randomizes everything that's not boss rooms, AND a mode where bosses could be randomized".
        """
        check = False
        rooms = {  # Format =>  World : highest room number 
                0:3,
                1:3,
                2:3,
                3:3,
                4:3,
                }
        while check is False:
            for i in range(0x186B5, 0x186BF+1 , 2):
                self[i] = random.randint(0,0x4)
                self[i+1] = random.randint(0,rooms[self[i]])
            dark_rooms = []
            for i in range(0x186B5, 0x186BF+1 , 2):
                dark_rooms.append((self[i], self[i+1]))
            for i in dark_rooms:
                if dark_rooms.count(i) == 1:
                    check = True
                else:
                    check = False
            print(dark_rooms)
            check = all([1 == dark_rooms.count(x) for x in dark_rooms])
            print(check)

    def exits_randomizer(self, fix_boss_exit, fix_locked_doors, keep_direction, pair_exits):

        # create world objects
        for world_i in [3]:
            this_world = World(self.data, world_i)
            this_world.showMap()
            this_world.randomizeExits(fix_boss_exit,fix_locked_doors,keep_direction,pair_exits)
            for i in range(this_world.exits.nExits):
                self[this_world.exits.offsets[i][0]] = this_world.exits.destination_frames[i]
                self[this_world.exits.offsets[i][4]] = this_world.exits.destination_Xpos[i]
                self[this_world.exits.offsets[i][5]] = this_world.exits.destination_Ypos[i]

        
        
