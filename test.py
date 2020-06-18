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
    hex(0x14137) : "Where the THE END should stop"
"""

# Format :
    # Nombre de "return"/Alignement/Nombre de lettres/couleur/Lettres x Nb/
    # FF will call the "THE END sprites if it's at "nombre de return"

def writetext(game, text,offset):


    for order, letter in enumerate(text):
        game[offset + order] = ord(letter.upper())

def credits_writter(game):
    #game[0x14137] = 30  # This works. It's where the THE END will stops"
    keeper = game[0x5FBC0:0x5FBD3 +1]  # These are the text that scrolls under the THE END


    free_credits_space = 0x5FBD4 - 0x5FDFF




with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    test_bosses(game)
    auto_bosses(game)


    credits_writter(game)

    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)