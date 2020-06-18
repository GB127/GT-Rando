from gameclass import ROM
from infos import *
import random
from changes import *
from debug import *
import datetime
info = infos()

# patrick gilmore
"""
for self.infos:
    hex(0x1414F) : "Speed of the THE END Credits",
    hex(0x14137) : "Where the THE END should stop if password used"
"""

# Format :
    # Nombre de "return"/Alignement/Nombre de lettres/couleur/Lettres x Nb/
    # FF will call the "THE END sprites if it's at "nombre de return"


# Credits ideas:
    # Developpers
    # Eventually, if it gets popular : discord link?


# Stats sccreen:
    # Version number
    # Flags
    # Worlds times
    # Deaths
    # Hits
    # Cherries
    # Bananas
    # Redd Gems
    # Blue Gems

def writetext(game, text,offset):
    for order, letter in enumerate(text):
        game[offset + order] = ord(letter.upper())

def credits_writter(game):
    vanilla_credits = game[0x5F99E:0x5FbbF +1]
    stats = game[0x5FBC0:0x5FBD3 +1]  # These are the text that scrolls under the THE END
    offset = 0x5f99D
    for value in vanilla_credits:  # Useless, since we rewrite everything back on it but hey I wrote it...
        offset += 1
        game[offset] = value
    for value in stats:
        offset += 1
        game[offset] = value

    offset += 1
    game.setmulti(offset, 0x5FDFF, 0x0)

with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    test_bosses(game)
    auto_bosses(game)


    text_writter(game)

    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)