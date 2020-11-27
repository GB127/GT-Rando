from gameclass import ROM, GT
import argparse
import random
from command import getoptions


def flag_string(options):
    flags = ""
    if options.Ricy:
        flags += "w"
    if options.Rdark:
        flags += "d"
    if options.Rfirst:
        flags += "f"
    if options.Rexits:
        flags += "e"
        if options.Rexits_matchdir is False:
            flags += "u"
        if options.Rexits_pair is False:
            flags += "U"
        if options.Ritems_pos:
            flags += "i"
            if options.Ritems:
                flags += "I"

    return flags


if __name__ == "__main__":
    options = getoptions()
    random.seed(options.seed)
    with open("Vanilla.smc", "rb") as original:  # We will have to change this to not force an exact filename.
        randogame = GT(original.read())
        randogame.passwordRandomizer()
        if options.Ricy:
            randogame.iceRandomizer()
        if options.Rdark:
            randogame.darkRandomizer()
        if options.Rfirst or options.Rexits or options.Ritems or options.Ritems_pos:
            randogame.randomizerWithVerification(options)


        flags = flag_string(options)
        with open(f"{flags}_{options.seed}.smc", "wb") as newgame:
            newgame.write(randogame.data)