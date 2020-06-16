def test_bosses(game):
    # This code currently changes only the 0-0 up exit to the boss.
    # Eventually it will support all 5 bosses for the 5 worlds.
    game[0x1F3ED] = 14

def level_select(game):
    # Put a banana on the box of the world you want to go    
        # Banana on the 2nd box = World 1 (2nd world of the game)
        # Banana on the 3rd box = World 2 (3rd world of the game)
    # Cherry for all the rest of the boxes

    Cherry = 0x0
    Banana = 0x1
    RedG = 0x2
    BlueG = 0x3
    password = [Cherry, Banana, RedG, BlueG]

    for i in range(0x1C67F, 0x1C692+1):
        game[i] = 0
            # I've started a new method in the class to allow setting multiple addresses.
            # The only current issue is the current written way don't make it random for each iteration.
            # Once that is fixed, these two lines can be replaced by one line.
        game[0x1c680] = 0x1
        game[0x1c686] = 0x1
        game[0x1c68c] = 0x1
        game[0x1c692] = 0x1