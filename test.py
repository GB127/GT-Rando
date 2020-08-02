from gameclass import ROM
from infos import *
import random
import datetime
info = infos()

with open("Vanilla.smc", "rb") as original:
    game = ROM(original.read())

    start = 0x1F3ED
    end = 0x1F4FF

    for i in range(start, end+1, 6):
        print(f"game[{hex(i)}] = {hex(game[i])}")


    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)

        