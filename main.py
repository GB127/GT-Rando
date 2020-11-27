from gameclass import ROM, GT
import argparse
import random
from command import getoptions


if __name__ == "__main__":
    options = getoptions()
    random.seed(options.seed)
    flags = ""  # Pour l'instant. On discutera après pour comment...
    with open("Vanilla.smc", "rb") as original:  # We will have to change this to not force an exact filename.
        randogame = GT(original.read())
        randogame.passwordRandomizer()
        if options.Wselect:
            random.choice(range(2))  # To increment the randomization to prevent cheating.
            randogame.activateWorldSelection()
        if options.Ricy:
            randogame.iceRandomizer()
            pass # Random icy rooms!
        if options.Rdark:
            randogame.darkRandomizer()
        if options.Rfirst or options.Rexits or options.Ritems or options.Ritems_pos:
            

        with open(f"{flags}_{options.seed}.smc", "wb") as newgame:
            newgame.write(randogame.data)