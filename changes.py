from infos import *
import random

def password_shuffler(game):
    """
        This is the password shuffler, to make sure one doesn't cheat.

        All password are shuffled and could be anything. Ther eis also a check to make sure
        That all worlds can be accessed (IE no 2 passwords are identical).

    Args:
        game : Data of the game Goof Troop

    Summary :
        randomize each box seperately
        check if each set of 5 are the same (one world is 5 boxes)
    """
    Cherry = 0x0
    Banana = 0x1
    RedG = 0x2
    BlueG = 0x3
    password = [Cherry, Banana, RedG, BlueG]

    check = False

    while check is False:
        # Actual randomization of the password
        for i in range(0x1C67F, 0x1C692+1):
            game[i] = random.choice(password)
                # I've started a new method in the class to allow setting multiple addresses.
                # The only current issue is the current written way don't make it random for each iteration.
                # Once that is fixed, these two lines can be replaced by one line.
        World_1_pass = [
                        game[0x1c67f],
                        game[0x1c680],
                        game[0x1c681],
                        game[0x1c682],
                        game[0x1c683]
                    ]
        World_2_pass = [
                        game[0x1c684],
                        game[0x1c685],
                        game[0x1c686],
                        game[0x1c687],
                        game[0x1c688]
                ]
        World_3_pass = [
                        game[0x1c689],
                        game[0x1c68a],
                        game[0x1c68b],
                        game[0x1c68c],
                        game[0x1c68d]
                ]
        World_4_pass = [
                        game[0x1c68e],
                        game[0x1c68f],
                        game[0x1c690],
                        game[0x1c691],
                        game[0x1c692]
                ]
        Worlds_passwords = [World_1_pass, World_2_pass, World_3_pass, World_4_pass]


        # Let's check if two passwords are identical
        for i in Worlds_passwords:
            if Worlds_passwords.count(i) == 1:
                check = True
            else:
                check = False
                # Do it again please.
                # (From my testing, it's very rare)

def darkrooms_randomizer(game):
    for i in range(0x186B5, 0x186BF+1 , 2):
        game[i] = random.randint(0,0x4)
    for i in range(0x186B6, 0x186C0+1 , 2):
        game[i] = random.randint(0,0xA)
    for i in range(0x186B5, 0x186BF +1,2):
        print(game[i], "-", game[i +1])
