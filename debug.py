from gameclass import GT
from gameclass import ROM

class debug(GT):
    def set_dark_room(self, world, room):
        # TODO: interactive
        self[0x186B5] = world
        self[0x186B6] = room

    def auto_bosses(self):
        # Currently only boss of world 4 (the pirate)
        self[0xC563] = 0x1

    def quick_bosses(self):
        self[0x1F3ED] = 14
        self[0x1F4C3] = 15
        self[0x1F58D] = 25
        # World 3 missing
        self[0x1f6f7] = 25
        self[0x1f6f7 + 4] = 180
        self[0x1F877] = 25

    def world_select(self):
        # Put a banana on the box of the world you want to go. Example  
            # Banana on the 3rd box = World 2 (3rd world of the game)
        # Cherry for all the rest of the boxes

        Cherry = 0x0
        Banana = 0x1
        RedG = 0x2
        BlueG = 0x3
        password = [Cherry, Banana, RedG, BlueG]

        self.setmulti(0x1C67F, 0x1C692, 0x0)
        self[0x1c680] = 0x1
        self[0x1c686] = 0x1
        self[0x1c68c] = 0x1
        self[0x1c692] = 0x1


with open("Vanilla.smc", "rb") as original:
    game = debug(original.read())
    game.world_select()


    with open("debug.smc", "wb") as newgame:
        newgame.write(game.data)
