from tools import gethex
from gameclass import ROM
from infos import *
import random
from changes import *

info = infos()


with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    darkrooms_randomizer(game)
    password_randomizer(game)
    game[0x6F72] = 0xA
    game[0x6F77] = 0xB

    with open("Vanillanoh.smc", "wb") as newgame:
        newgame.write(game.data)