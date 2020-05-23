from tools import gethex
from gameclass import ROM
from infos import *
import random

info = infos()

gethex(0xA9)



with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)

    # These two lines will mess with all the "get items"
    # so you will always get the same item everytime!
    # This is a step toward the randomization of the items.
    # But this tells me that changing items will be simple.
    # In summary, the functions only need one value and does all
    # the dirty works. Note that I've changed some stuffs to make
    # it load the thing I want.

    # Only need to find the roots how the thing it normally loads is changed.
    game[0x13067] = 169
    game[0x13068] = random.choice([0,2,4,6,8,10,12])

    with open("vanillanoh.smc", "wb") as newgame:
        newgame.write(game.data)