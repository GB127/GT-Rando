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
        randogame.add_credits() # Will be gone since it the function will be included in the init directly.

        if options.Rpass:
            randogame.password_randomizer()
        if options.Rfirst:
            pass # Random First frame!
        if options.Ricy or options.RicyV:
            # Ricy is if we have more than 2 icy rooms.
            # RicyV is if we keep 2 icy rooms.
            pass # Random icy rooms!
        if options.Rdark or options.RdarkV:
            # Rdark is if we have more than 6 dark rooms.
            # RdarkV is if we keep 6 dark rooms.
            pass  # Random dark rooms!
        if options.Rfirst:
            pass  # Random first frame!
        if options.Exits:
            pass  # Random exits! using the other options, see command.py
        if options.Items:
            pass

        with open(f"{flags}_{options.seed}.smc", "wb") as newgame:
            newgame.write(randogame.data)