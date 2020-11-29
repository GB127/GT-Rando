import argparse
import random

def getoptions():

    parser = argparse.ArgumentParser(description="Goof Troop Randomizer, Version 1.0", epilog="Written by Guylain Breton & Charles Matte-Breton")


    # Dark rooms
        # Logic : big D => May be higher than 6, thus capital letter
    parser.add_argument("-d", "--dark", action="store_true",
    help="Randomize which rooms are dark, same amount of dark rooms as vanilla (6)", dest="Rdark")

    parser.add_argument("-D", "--Vdark", action="store_true",
    help="Randomize which rooms are dark, random & higher count than vanilla", dest="Rverydark")


    # Icy rooms
        # Logic : W for winter, winter = snow and ice, thus icy rooms!
        # Logic : big W => May be higher than 2, thus capital letter
    parser.add_argument("-w", "--icy", action="store_true",
    help="Randomize which rooms are icy, same amount of icy rooms as vanilla (2)", dest="Ricy")

    parser.add_argument("-W", "--Vicy", action="store_true",
    help="Randomize which rooms are icy,random & higher count than vanilla", dest="Rveryicy")


    # First frame randomizer
    parser.add_argument("-f", "--first", action="store_true",
    help="Randomize the frame where you start for each world", dest="Rfirst")

    # Exits
    parser.add_argument("-e", "--exits", action="store_true",
    help="Randomize the exits", dest="Rexits")
    parser.add_argument("-u", "--unmatchdir", action="store_false",
    help="Do not match the direction for the exits and their destination", dest="Rexits_matchdir")
    parser.add_argument("-U", "--unpair", action="store_false",
    help="Do not pair exits. Be careful not to get stuck!", dest="Rexits_pair")
    

    # Items
    parser.add_argument("-i", "--itemsshuff", action="store_true",
    help="Shuffle the items, each world keeps its items pool", dest="Ritems_pos")
    parser.add_argument("-I", "--items", action="store_true",
    help="Completely random items. You might have to shovel your way through the dark rooms ;)", dest="Ritems")

    # Seed
    parser.add_argument("--seed", action="store", help="Seed for the randomization",
                        dest="seed", default=str(random.random())[2:], metavar="", type=str)

    # Password cheat
    parser.add_argument("--worldselect", action="store_true",
    help="Allows to select the world of your choice with a banana...", dest="Wselect")
    
    options = parser.parse_args()
    analyse_options(options)
    return options

def analyse_options(options):

    if any([not options.Rexits_matchdir,not options.Rexits_pair]) and (options.Rexits is False):
        raise BaseException("Unmatching exits direction (u) and unpairing the exits (U) must be used with the exits randomizer (e)")
    if all([options.Rdark, options.Rverydark]):
        raise BaseException("Cannot use d and D at the same time.")
    if all([options.Ricy, options.Rveryicy]):
        raise BaseException("Cannot use w and W at the same time.")
    if all([options.Ritems, options.Ritems_pos]):
        raise BaseException("Cannot use i and I at the same time.")


if __name__ == "__main__":
    test = getoptions()
    print(test.Ritems_random)