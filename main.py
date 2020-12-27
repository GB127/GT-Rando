from gameclass import ROM, GT, RandomizerError
import argparse
import random
from command import getoptions


def flag_string(options):
    flags = ""
    if options.Ricy:
        flags += "s"
    elif options.Rveryicy:
        flags += "S"
    if options.Rdark:
        flags += "d"
    elif options.Rverydark:
        flags += "D"
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
    if options.Ralert:
        flags += "a"
    if options.Rveryalert:
        flags += "A"

    return flags




if __name__ == "__main__":
    options = getoptions()

    random.seed(options.seed)
    flags = flag_string(options)

    with open("Vanilla.smc", "rb") as original:  # We will have to change this to not force an exact filename.
        randogame = GT(original.read(), options.seed)
        randogame.passwordRandomizer()
        if options.Wselect:
            randogame.activateWorldSelection()
        if options.Ricy:
            randogame.iceRandomizer()
        if options.Rveryicy:
            tempo = int(random.gauss(12,5))
            while tempo < 7:
                tempo = int(random.gauss(7,5))
            randogame.iceRandomizer(count=tempo)
        if options.Aicy:
            randogame.allIcy()
        if options.noicy:
            randogame.no_icy()
        if options.Rdark:
            randogame.darkRandomizer()
        if options.Rverydark:
            tempo = int(random.gauss(12,5))
            while tempo < 7:
                tempo = int(random.gauss(7,5))
            randogame.darkRandomizer(count=tempo)
        if options.Adark:
            randogame.allDark()
        if options.nodark:
            randogame.no_dark()

        """
        if options.Ralert:
            randogame.alert_Randomizer()
        if options.Rveryalert:
            #tempo = int(random.gauss(12,5))
            tempo = 90
            while tempo < 7:
                tempo = int(random.gauss(7,5))
            randogame.alert_Randomizer(count=tempo)


        if options.Aalert:
            randogame.allAlert()
        """

        if not options.Rexits_matchdir:
            randogame.fix_misdirection()

        if options.Rfirst or options.Rexits or options.Ritems_pos or options.Ritems:
            if options.Rfirst: randogame.modify_data_starting_frame()  # Changement du code pour permettre une randomization du first frame.
            try:
                randogame.randomizerWithVerification(options)
            except RandomizerError:
                with open("error_flags_seed.txt", "a") as report:
                    report.write(f'python main.py -{flags} --seed {options.seed}\n')
                    flags += "_ERROR"

        if options.ohko:
            randogame.ohko()

        randogame.credits_frames_randomizer()
        randogame.checksum(options.Adark, options.Aicy, options.ohko)
        with open(f"GT_{flags}_{options.seed}.smc", "wb") as newgame:
            newgame.write(randogame.data)