from gameclass import ROM
import argparse
from changes import *
import random

def getoptions():
    parser = argparse.ArgumentParser(description="Goof Troop Randomizer, Version alpha", epilog="Written by Niamek & Charles342")

    parser.add_argument("-d", "--dark", action="store_true",
    help="Randomize which rooms are dark", dest="Rdark")

    parser.add_argument("--password", action="store_false",
    help="Disable the password randomization", dest="Rpass")
    return parser.parse_args()

    parser.add_argument("--seed", action="store", help="Seed for the randomization",
                        dest="seed", default=random.random(), metavar="", type=int)


if __name__ == "__main__":
    options = getoptions()
    seed = str(options.seed)[2:] if options.seed < 1 else options.seed
        # Note that this isn't used anywhere yet.
    with open("Vanilla.smc", "rb") as original:
        originaldata = original.read()
        randogame = ROM(originaldata)
        add_credits(randogame)
        if options.Rpass:
            password_randomizer(randogame)
        if options.Rdark:
            darkrooms_randomizer(randogame)
        with open("vanillanoh.smc", "wb") as newgame:
            newgame.write(randogame.data)