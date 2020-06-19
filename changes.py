from infos import *
import random

def add_credits(game):
    """
        This function will add the credits of the contributors of this project
        in the credits of the game. It defines a function internally, then uses it for each lines.
    """

    def add_credits_line(game, text,*, center=True, color=0, underlined=False, spacing=0xD):
        """ This function will add a single line to the credits of the game.

        Args:
            game ([type]): [description]
            text (str) : The text to be written. Max 32 characters as it's the width of the screen.
            center (bool, optional): Centered text or not. Defaults to True.
            color (int, optional): Color, must be 0-15 currently. Defaults to 0 (white).
            underlined (bool, optional): Will underline the words. Defaults to False.
            spacing (int, optional): Vertical spacing. Defaults to 0xD.
        """

        assert len(text) <= 32, f"Text line too long ({len(text)}). Must be < 32"
        assert color <= int("1111", base=2), "0 < Color < 0" # FIXME : I tried to check if color < 0, but couldn't make it work.

        credits_range = game[0x5F99E: 0x5FFFF +1]  
            # This is the entire range available for writting the credits... Almost. 
            # I did not make sure it won't scrap the palettes that are stored futher in the region.
            # Eventually I'll try to fix that. But it seems daunting and tedious... And I'm tired to watch the credits :P
        offset = credits_range.index(0xFF) + 0x5F99E
            # 0xFF will call the "THE END sprites if it's at "nombre de return"
            # In other words, this will fetch the end of the current credits.
        stats = game[offset: offset +20]
            # After the credits, the total time is there. I need to keep them, so I created
            # a new variable.

        game[offset] = spacing  # Nb de returns (vertical spacing)
        offset += 1
        game[offset] = 16 - len(text) // 2 if center else 1 # Horizontal Alignement
        offset += 1
        game[offset] = len(text)  # nombre de lettres
        offset += 1
        game[offset] = color * 4
                # byte 0 displayed the text weirdly (jap?)
                # byte 1 displayed nothing => If set, always display nothing?
                # byte 7-8 : Mirrors stuffs
                # All the others are colors stuffs

                # By multiplying by 4, we are doing two shift left and 
                # then dodge the bits 0 and bits 1 being set.
                # Since we can't have bits 7 and 8 set as well, we then cannot
                # have an initial color higher than 15 (in binary : 1111).
        for letter in text:  # Writting the string
            offset += 1
            game[offset] = ord(letter.upper())
        for value in stats:
            offset += 1
            assert offset <= 0x5FFFF, "Too much text added"  # This is the check to make sure we don't pass the allowed range.
                # Currently, we can write up to the end of the bank, overwritting the palettes section.
            game[offset] = value
        if underlined:
            # An underline is simply a new line with "¨".
            string = "¨" * len(text)
            add_credits_line(game,string ,center=center, color=color, spacing=0x1)

    add_credits_line(game, "Goof Troop randomizer", underlined=True, color=4)
    add_credits_line(game, "Version alpha", spacing=1)
    add_credits_line(game, "Flags used : alpha", spacing=1)
    add_credits_line(game, "Developpers", underlined=True, color=5)
    add_credits_line(game, "GB127 - Niamek", spacing=2)
    add_credits_line(game, "Charles342", spacing=2)
    add_credits_line(game, "Special thanks", underlined=True, color=3)
    add_credits_line(game, "PsychoManiac", spacing=2)

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

        # Let's check if two passwords are identical
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

