from debug import debug
from copy import deepcopy

def getters_doors(data, world, frame):  #82C329
    """ À l'initialisation du monde, les offsets 1144 et 1145 sont settés à 0.
        """

    liste = []
    this_world_frame_offset = data[0x14461 + world] + frame
    offset_Y_1 = data[0x14461 + this_world_frame_offset]
    if offset_Y_1 != 0:
        offset_base = data[0x144D7 + offset_Y_1]
        # REP #31
        current_offset = (offset_base & 0x00FF) + 0xC4D8
        # SEP #20
        count = data[0x8000 + current_offset]
        if count != 0:
            current_offset += 1
            for _ in range(count):
                door_data = data[0x8003 + current_offset]
                which_door = 0x1144 + int((door_data & 0x7F) / 2 / 2 / 2)

                bit_offset = door_data & 0x07
                bit_to_check = data[0x180B8 + bit_offset]
                liste.append((hex(which_door), bin(bit_to_check)))
                    # For now it will be this.
                    # To have a number instead of strings, just remove the functions.
                    # For now, we'll keep this, because I need to visualise my stuffs.

                # REP 21
                # This has been done earlier in the code for some reason.
                something_OxA = data[0x8002 + current_offset]

                # Preparation just before calling the door remover
                something_x13_X = data[0x8000 + current_offset]
                something_0x22 = deepcopy(current_offset)
                #door_remover(data, something_OxA, something_0x22)

                current_offset += 4
    return liste



# 82C3BE : Door remover!!!!! Donc, de ce que j'en comprends, les portes sont préplacés, et on les enlèves à chaque fois.
    # Cette fonctione nlève aussi les portes de 1146. C'est donc une enleveuse de portes universelle.

def door_remover(data, A, Ox22):
    something_0xA = A // 2 # LSR
    offset_X_1 = something_0xA  # TAX

    something_0 = data[0x14452 + offset_X_1] // 2 // 2 // 2 // 2

    something_2_6 = data[0x14452 + offset_X_1] & 0xF





with open("Vanilla.smc", "rb") as original:
    game = debug(original.read())
    getters_doors(game.data, 0, 5)

