from gameclass import ROM

with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    randogame = ROM(originaldata)
    with open("vanillanoh.smc", "wb") as newgame:
        newgame.write(randogame.data)