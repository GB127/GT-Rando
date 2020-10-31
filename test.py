from gameclass import ROM
from infos import *
import random
import datetime
info = infos()

with open("Vanilla.smc", "rb") as original:
    game = ROM(original.read())

    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)

        