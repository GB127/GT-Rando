from gameclass import ROM
from infos import *
import random
from changes import *
from debug import *

info = infos()


# patrick gilmore
"""
for self.infos:
    hex(0x1414F) : "Speed of the THE END Credits"
"""


def writetext(game, text,offset):
    for order, letter in enumerate(text):
        game[offset + order] = ord(letter.upper())

with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    test_bosses(game)
    auto_bosses(game)


    game[0x1414F] = 0xFF
    with open("Vanillanoh.smc", "wb") as newgame:
        print("Testing case have been created!")
        newgame.write(game.data)