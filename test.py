from tools import gethex
from gameclass import ROM
from infos import *
import random
from changes import *

info = infos()


with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    password_shuffler(game)
    with open("Vanillanoh.smc", "wb") as newgame:
        newgame.write(game.data)