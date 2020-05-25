from tools import gethex
from gameclass import ROM
from infos import *
import random

info = infos()

items = [0x8,0x9,0xA,0xB,0xC,0xD,0xE]


with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    game = ROM(originaldata)
    game[0x6F69] = random.choice(items)
    game[0x6F72] = random.choice(items)
    game[0x6F77] = random.choice(items)
    game[0x6F7C] = random.choice(items)
    game[0x6F8D] = random.choice(items)
    game[0x6F9F] = random.choice(items)
    game[0x6FB1] = random.choice(items)
    game[0x6FC3] = random.choice(items)
    game[0x6FCC] = random.choice(items)
    game[0x6FDD] = random.choice(items)
    game[0x7013] = random.choice(items)
    game[0x7018] = random.choice(items)
    game[0x701C] = random.choice(items)
    game[0x7022] = random.choice(items)
    game[0x7027] = random.choice(items)
    game[0x702B] = random.choice(items)
    game[0x7034] = random.choice(items)
    game[0x7038] = random.choice(items)
    game[0x7043] = random.choice(items)
    game[0x7048] = random.choice(items)
    game[0x7050] = random.choice(items)
    game[0x7055] = random.choice(items)
    game[0x7072] = random.choice(items)
    game[0x7077] = random.choice(items)
    game[0x707C] = random.choice(items)
    game[0x70DB] = random.choice(items)
    game[0x70E0] = random.choice(items)
    game[0x70E5] = random.choice(items)
    game[0x7080] = random.choice(items)
    game[0x7084] = random.choice(items)
    game[0x708E] = random.choice(items)
    game[0x7092] = random.choice(items)
    game[0x70BA] = random.choice(items)
    game[0x70BE] = random.choice(items)
    game[0x70C2] = random.choice(items)
    game[0x70CC] = random.choice(items)
    game[0x70D6] = random.choice(items)
    game[0x7101] = random.choice(items)
    game[0x7107] = random.choice(items)
    game[0x707D] = random.choice(items)
    game[0x70EB] = random.choice(items)
    game[0x70EF] = random.choice(items)
    game[0x70F5] = random.choice(items)
    game[0x7122] = random.choice(items)
    game[0x7126] = random.choice(items)
    game[0x7171] = random.choice(items)
    game[0x719D] = random.choice(items)
    game[0x71A6] = random.choice(items)
    game[0x71D2] = random.choice(items)
    game[0x71E2] = random.choice(items)
    game[0x71EA] = random.choice(items)
    game[0x71F8] = random.choice(items)
    game[0x71FC] = random.choice(items)
    game[0x720B] = random.choice(items)
    game[0x720F] = random.choice(items)
    game[0x721D] = random.choice(items)
    game[0x7221] = random.choice(items)
    game[0x7225] = random.choice(items)
    game[0x723A] = random.choice(items)
    game[0x7260] = random.choice(items)
    game[0x7264] = random.choice(items)
    game[0x726D] = random.choice(items)
    game[0x7272] = random.choice(items)
    game[0x727C] = random.choice(items)
    game[0x7297] = random.choice(items)
    game[0x729B] = random.choice(items)    
    with open("Vanillanoh.smc", "wb") as newgame:
        newgame.write(game.data)