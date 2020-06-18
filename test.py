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
    # Red Gems
    # Blue Gems

def add_credits(game, text):

    credits_range = game[0x5F99E: 0x5FFFF +1]
    offset = credits_range.index(0xFF) + 0x5F99E
    print(hex(offset))
    stats = game[offset: offset +20]


    game[offset] = 0x02
    offset += 1
    assert offset < 0x5FFFF, "Too much text"
    game[offset] = 0x04
    offset += 1
    assert offset < 0x5FFFF, "Too much text"
    game[offset] = len(text)
    offset += 1
    assert offset < 0x5FFFF, "Too much text"
    game[offset] = 0x30
    for letter in text:
        offset += 1
        assert offset < 0x5FFFF, "Too much text"
        game[offset] = ord(letter.upper())
    for value in stats:
        offset += 1
        assert offset < 0x5FFFF, "Too much text"
        game[offset] = value


with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    test_bosses(game)
    auto_bosses(game)

    add_credits(game,"Allo Charles, je suis vraiment tanné")
    add_credits(game,"de regarder les credits")
    add_credits(game,"pour vérifier si mon code marche")
    add_credits(game,"et ceci est la preuve que ça marche")
    add_credits(game,"Enjoy!")

    add_credits(game,"pour vérifier si mon code marche")
    add_credits(game,"et ceci est la preuve que ça marche")
    add_credits(game,"Enjoy!")

    add_credits(game,"pour vérifier si mon code marche")






    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)