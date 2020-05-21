from gameclass import ROM
from checker import gamechecker

with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    randogame = ROM(originaldata)
    gamechecker(randogame)
    with open("test.smc", "wb") as newgame:
        newgame.write(randogame.data)