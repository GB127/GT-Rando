from gameclass import ROM
from infos import *
import random
from changes import *
from debug import *
import datetime
info = infos()

# Je me suis permis d'ajouter ceci dans ton propre fichier de sorte que tu aies ton test.py. ^^


with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)

    with open("Vanillanoh.smc", "wb") as newgame:
        print(f"Testing case have been created! {datetime.datetime.now()}")
        newgame.write(game.data)