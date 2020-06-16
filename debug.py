def dark_room(game, world, room):
    # Currently this sets the darkness in the specific room.
    game[0x186B5] = world
    game[0x186B6] = room

def test_bosses(game):
    # This code currently changes only the 0-0 up exit to the boss.
    # Eventually it will support all 5 bosses for the 5 worlds.
    game[0x1F3ED] = 14

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