from gameclass import ROM
from infos import *
import random
from debug import *
import datetime
info = infos()

with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)

    start = 0x1F3ED
    end = 0x1F4FF

    for i in range(start, end+1, 6):
        print(f"game[{i}] = {hex(game[i])}")


    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)

        