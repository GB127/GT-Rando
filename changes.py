from infos import *
import random

def password_randomizer(game):
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
        check = all([1 == Worlds_passwords.count(x) for x in Worlds_passwords])



def darkrooms_randomizer(game):
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
            game[i] = random.randint(0,0x4)
            game[i+1] = random.randint(0,rooms[game[i]])
        dark_rooms = []
        for i in range(0x186B5, 0x186BF+1 , 2):
            dark_rooms.append((game[i], game[i+1]))
        for i in dark_rooms:
            if dark_rooms.count(i) == 1:
                check = True
            else:
                check = False
        print(dark_rooms)
        check = all([1 == dark_rooms.count(x) for x in dark_rooms])
        print(check)

