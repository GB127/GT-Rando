from tools import gethex
from gameclass import ROM
from infos import *
import random
from changes import *
from debug import *

info = infos()


with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    level_select(game)
    with open("Vanillanoh.smc", "wb") as newgame:
        print("Testing case have been created!")
        newgame.write(game.data)