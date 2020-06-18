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


def writetext(game, text,offset):
    for order, letter in enumerate(text):
        game[offset + order] = ord(letter.upper())

def improve_credits(game):
    game[0x14137] = 30  # This works




with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    test_bosses(game)
    auto_bosses(game)

    game.setmulti(0x14068,0x1406B, 0xEA)

    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)