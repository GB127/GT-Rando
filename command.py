import argparse
import random

def getoptions():
    parser = argparse.ArgumentParser(description="Goof Troop Randomizer, Version alpha", epilog="Written by Guylain Breton & Charles Matte-Breton")


    # Dark rooms
        # S for shadow, without shadow there is no dark!
        # Logic : big D => May be higher than 6, thus capital letter
    parser.add_argument("-S", "--dark", action="store_true",
    help="Randomize which rooms are dark", dest="Rdark")
    parser.add_argument("-s", "--darkV", action="store_true",
    help="Randomize which rooms are dark, same amount of dark rooms as vanilla (6)", dest="RdarkV")

    # Icy rooms
        # Logic : W for winter, winter = snow and ice, thus icy rooms!
        # Logic : big I => May be higher than 2, thus capital letter
    parser.add_argument("-W", "--icy", action="store_true",
    help="Randomize which rooms are icy", dest="Ricy")
    parser.add_argument("-w", "--icyV", action="store_true",
    help="Randomize which rooms are icy, same amount of icy rooms as vanilla (2)", dest="RicyV")

    # First frame randomizer
    parser.add_argument("-f", "--first", action="store_true",
    help="Randomize the first level of each world", dest="Rfirst")

    # Exits
    parser.add_argument("-E", "--exits", action="store_true",
    help="Randomize the exits", dest="Rexits")
    parser.add_argument("-B", "--bossE", action="store_false",
    help="Include the boss exits in the exits pool", dest="Rexits_B")
    parser.add_argument("-X", "--xexits", action="store_false",
    help="Do not keep directions", dest="Rexits_X")
    parser.add_argument("-2", "--pairs", action="store_false",
    help="Do not pair exits", dest="Rexits_2")


    # Items
    # This is done!
    parser.add_argument("-I", "--items", action="store_true",
    help="Randomize the items, each world keep their items pool", dest="Ritems")
    parser.add_argument("-Q", "--Ritems", action="store_false",
    help="Completely random items", dest="Ritems_random")
    parser.add_argument("-c", "--candle", action="store_true",
    help="Make sure you have a candle in a world that has at least one dark room", dest="dark_candle")

    # Seed
    parser.add_argument("--seed", action="store", help="Seed for the randomization",
                        dest="seed", default=str(random.random())[2:], metavar="", type=int)

    # Password random
    parser.add_argument("--password", action="store_false",
    help="Disable the password randomization", dest="Rpass")
    
    options = parser.parse_args()
    analyse_options(options)
    return options

def analyse_options(options):
    if options.Ritems_random: options.Ritems = True

    # Pour ceci, il y aura des changements à faire. 
    # Mais l'idée est là...

    #if any([options.Rexits_B, options.Rexits_X, options.Rexits_2]) and (options.Rexits is False):
    #    raise BaseException("Exit randomizer flag must be used if blablabla")
    #if options.Ritems_random and (options.Ritems is False):
    #    raise BaseException("Completely random items must be used with The random items flag (I)")


    # Ci-desssous devrait fonctionner.
    if options.Rdark and options.RdarkV:
        raise BaseException("Can't have S and s set at the same time.")
    if options.Ricy and options.RicyV:
        raise BaseException("Can't have W and w set at the same time.")



if __name__ == "__main__":
    test = getoptions()
    print(test.Ritems_random)