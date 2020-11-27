from gameclass import ROM, GT, RandomizerError
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
    flags = flag_string(options)

    with open("Vanilla.smc", "rb") as original:  # We will have to change this to not force an exact filename.
        randogame = GT(original.read())
        randogame.passwordRandomizer()
        if options.Ricy:
            randogame.iceRandomizer()
        if options.Rdark:
            randogame.darkRandomizer()
        if options.Rfirst or options.Rexits or options.Ritems_pos:
            try:
                randogame.randomizerWithVerification(options)
            except RandomizerError:
                with open("error_flags_seed.txt", "a") as report:
                    report.write(f'python main.py -{flags} --seed {options.seed}\n')
                    flags += "_ERROR"
        with open(f"{flags}_{options.seed}.smc", "wb") as newgame:
            newgame.write(randogame.data)