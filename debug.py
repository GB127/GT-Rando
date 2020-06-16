def test_boss_w0(game):
    # This code changes 0-0 up exit to the boss.
    game[0x1F3ED] = 14

def easy_pass(game):
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