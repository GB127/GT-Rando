from infos import *

info = infos()

info.listadresses("Password")

def password_shuffler(game):
    Cherry = 0x0
    Banana = 0x1
    RedG = 0x2
    BlueG = 0x3
    password = [Cherry, Banana, RedG, BlueG]
    World_1 = [
                game[0x1c67f],
                game[0x1c680],
                game[0x1c681],
                game[0x1c682],
                game[0x1c683]
            ]
    World_2 = [
                game[0x1c684],
                game[0x1c685],
                game[0x1c686],
                game[0x1c687],
                game[0x1c688]
            ]
    World_3 = [
                game[0x1c689],
                game[0x1c68a],
                game[0x1c68b],
                game[0x1c68c],
                game[0x1c68d]
            ]
    World_4 = [
                game[0x1c68e],
                game[0x1c68f],
                game[0x1c690],
                game[0x1c691],
                game[0x1c692]
            ]