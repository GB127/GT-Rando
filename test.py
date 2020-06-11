from tools import gethex
from gameclass import ROM
from infos import *
import random

info = infos()



with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)




    with open("Vanillanoh.smc", "wb") as newgame:
        newgame.write(game.data)