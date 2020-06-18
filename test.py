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
# Stats screen:
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
    # Format :
    # Nombre de "return"/Alignement/Nombre de lettres/couleur/Lettres x Nb/
    # FF will call the "THE END sprites if it's at "nombre de return"
    assert len(text) <= 32, f"Text line too long ({len(text)}). Must be < 32"


    credits_range = game[0x5F99E: 0x5FFFF +1]
    offset = credits_range.index(0xFF) + 0x5F99E
    stats = game[offset: offset +20]

    game[offset] = 0x04  # Nb de returns
    offset += 1
    assert offset < 0x5FFFF, "Too much text added"
    game[offset] = 0x00  # Alignement
    offset += 1
    assert offset < 0x5FFFF, "Too much text added"
    game[offset] = len(text)
    offset += 1
    assert offset < 0x5FFFF, "Too much text added"
    game[offset] = 0x30
    for letter in text:
        offset += 1
        assert offset < 0x5FFFF, "Too much text added"
        game[offset] = ord(letter.upper())
    for value in stats:
        offset += 1
        assert offset < 0x5FFFF, "Too much text added"
        game[offset] = value


with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    test_bosses(game)
    auto_bosses(game)

    add_credits(game, "Allo charles!")

    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)