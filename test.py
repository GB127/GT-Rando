from gameclass import ROM
from infos import *
import random
from changes import *
from debug import *
import datetime
info = infos()


def add_credits(game):
    def add_credits_line(game, text,*, center=True, color=0, underlined=False, spacing=0xD):
        assert len(text) <= 32, f"Text line too long ({len(text)}). Must be < 32"
        assert color <= int("1111", base=2), "0 < Color < 0"

        credits_range = game[0x5F99E: 0x5FFFF +1]
        offset = credits_range.index(0xFF) + 0x5F99E
        stats = game[offset: offset +20]

        game[offset] = spacing  # Nb de returns
            # FF will call the "THE END sprites if it's at "nombre de return"
        offset += 1
        game[offset] = 16 - len(text) // 2 if center else 1 # Alignement
        offset += 1
        game[offset] = len(text)  # nombre de lettres
        offset += 1
        game[offset] = color * 4
                # byte 0 displayed the text weirdly (jap?)
                # byte 1 displayed nothing => If set, always display nothing?
                # byte 7-8 : Mirrors stuffs
                # All the others are colors stuffs
        for letter in text:
            offset += 1
            game[offset] = ord(letter.upper())
        for value in stats:
            offset += 1
            assert offset <= 0x5FFFF, "Too much text added"
            game[offset] = value
        if underlined:
            string = "¨" * len(text)
            add_credits_line(game,string ,center=center, color=color, spacing=0x1)
    add_credits_line(game, "Goof Troop randomizer", underlined=True, color=4)
    add_credits_line(game, "Version alpha", spacing=1)
    add_credits_line(game, "Flags used : alpha", spacing=1)
    add_credits_line(game, "Developpers", underlined=True, color=5)
    add_credits_line(game, "GB127 - Niamek", spacing=2)
    add_credits_line(game, "Charles342", spacing=2)

    add_credits_line(game, "Special thanks", underlined=True, color=3)
    add_credits_line(game, "PsychoManiac", spacing=2)


with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    test_bosses(game)
    auto_bosses(game)
    add_credits(game)


    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)