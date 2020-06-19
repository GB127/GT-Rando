from gameclass import ROM
from infos import *
import random
from changes import *
from debug import *
import datetime
info = infos()





with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)

    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)