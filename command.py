import argparse
import random

def getoptions():
    parser = argparse.ArgumentParser(description="Goof Troop Randomizer, Version alpha", epilog="Written by Guylain Breton & Charles Matte-Breton")


    # Dark rooms
        # S for shadow, without shadow there is no dark!
        # Logic : big S => May be higher than 6, thus capital letter
    parser.add_argument("-d", "--dark", action="store_true",
    help="Randomize which rooms are dark, same amount of dark rooms as vanilla (6)", dest="Rdark")
    parser.add_argument("-D", "--verydark", action="store_true",
    help="Randomize which rooms are dark. For those who like playing around with darkness", dest="Rverydark")

    # Icy rooms
        # Logic : W for winter, winter = snow and ice, thus icy rooms!
        # Logic : big W => May be higher than 2, thus capital letter
    parser.add_argument("-w", "--icy", action="store_true",
    help="Randomize which rooms are icy, same amount of icy rooms as vanilla (2)", dest="Ricy")
    parser.add_argument("-W", "--veryicy", action="store_true",
    help="Randomize which rooms are icy. For those who like playing around with the weather", dest="Rveryicy")

    # First frame randomizer
    parser.add_argument("-f", "--first", action="store_true",
    help="Randomize the frame where you start for each world", dest="Rfirst")

    # Exits
    parser.add_argument("-e", "--exits", action="store_true",
    help="Randomize the exits", dest="Rexits")
    parser.add_argument("-u", "--unmatchdir", action="store_false",
    help="Do not match the direction for the exits and their destination", dest="Rexits_X")
    parser.add_argument("-U", "--unpair", action="store_false",
    help="Do not pair exits. Be careful not to get lost!", dest="Rexits_2")
    parser.add_argument("-b", "--preboss", action="store_false",
    help="Include the exit leading to the boss in the exits pools", dest="Rexits")

    # Items
    parser.add_argument("-i", "--items", action="store_true",
    help="Randomize the items, each world keeps its items pool", dest="Ritems")
    parser.add_argument("-I", "--Ritems", action="store_false",
    help="Completely random items. You might have to shovel your way through the dark rooms ;)", dest="Ritems_random")

    # Seed
    parser.add_argument("-s","--seed", action="store", help="Seed for the randomization",
                        dest="seed", default=str(random.random())[2:], metavar="", type=str)

    # Password cheat
    parser.add_argument("--worldselect", action="store_true",
    help="Allows to select the world of your choice with a banana...", dest="Dselect")
    
    options = parser.parse_args()
    analyse_options(options)
    return options

def analyse_options(options):
    if options.Ritems_random and not options.Ritems:
        raise BaseException("Completely random items randomizer (I) must be used with the item randomizer (i)")
    # B,X,2  Need #E
    if any([not options.Rexits_B,not options.Rexits_X,not options.Rexits_2]) and (options.Rexits is False):
        raise BaseException("Boss exits in pools (b), unmatching exits direction (u) and unpairing the exits (U) must be used with the exits randomizer (e)")

    # Q needs I
    if not options.Ritems_random and (options.Ritems is False):
        raise BaseException("Completely random items must be used with The items randomizer (I)")


    # Ci-desssous devrait fonctionner.
    if options.Rdark and options.RdarkV:
        raise BaseException("Can't have S and s set at the same time.")
    if options.Ricy and options.RicyV:
        raise BaseException("Can't have W and w set at the same time.")



if __name__ == "__main__":
    test = getoptions()
    print(test.Ritems_random)