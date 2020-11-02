from gameclass import ROM, GT
import argparse
import random

def getoptions():
    parser = argparse.ArgumentParser(description="Goof Troop Randomizer, Version alpha", epilog="Written by Niamek & Charles342")

    parser.add_argument("-d", "--dark", action="store_true",
    help="Randomize which rooms are dark", dest="Rdark")

    parser.add_argument("--password", action="store_false",
    help="Disable the password randomization", dest="Rpass")

    parser.add_argument("--seed", action="store", help="Seed for the randomization",
                        dest="seed", default=random.random(), metavar="", type=int)
    return parser.parse_args()


if __name__ == "__main__":
    options = getoptions()
    random.seed(str(options.seed)[2:] if options.seed < 1 else options.seed)
        # Note that this isn't used anywhere yet.
    with open("Vanilla.smc", "rb") as original:
        originaldata = original.read()
        randogame = GT(originaldata)
        randogame.add_credits()
        if options.Rpass:
            randogame.password_randomizer()
        if options.Rdark:
            randogame.darkrooms_randomizer()
        with open("vanillanoh.smc", "wb") as newgame:
            newgame.write(randogame.data)