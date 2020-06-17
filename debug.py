def dark_room(game, world, room):
    # Currently this sets the darkness in the specific room.
    game[0x186B5] = world
    game[0x186B6] = room

def test_bosses(game):
    level_select(game)
    game[0x1F3ED] = 14
    game[0x1F4C3] = 15
    game[0x1F58D] = 25
    # World 3 missing
    game[0x1F877] = 25

def level_select(game):
    # Put a banana on the box of the world you want to go. Example  
        # Banana on the 3rd box = World 2 (3rd world of the game)
    # Cherry for all the rest of the boxes

    Cherry = 0x0
    Banana = 0x1
    RedG = 0x2
    BlueG = 0x3
    password = [Cherry, Banana, RedG, BlueG]

    game.setmulti(0x1C67F, 0x1C692, 0x0)
    game[0x1c680] = 0x1
    game[0x1c686] = 0x1
    game[0x1c68c] = 0x1
    game[0x1c692] = 0x1