from tools import gethex
from gameclass import ROM
from infos import *
import random

info = infos()

gethex(0xA9)  # 169
gethex(0xE8)  # 232
gethex(0xEA)  # 234


with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)

    game[0x65DC] = 0xA9
    game[0x65DD] = 0xE8
    game[0x65DE] = 0xEA

    with open("vanillanoh.smc", "wb") as newgame:
        newgame.write(game.data)