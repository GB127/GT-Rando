from tools import gethex
from gameclass import ROM
from infos import *
import random

info = infos()



with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)

    game[0x65DC] = 0xA9
    game[0x65DD] = 0xE
    game[0x65DE] = 0xEA



    # 3 = Gold key

    with open("vanillanoh.smc", "wb") as newgame:
        newgame.write(game.data)