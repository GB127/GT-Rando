from copy import deepcopy

def getters_doors(data, world, frame):  #82C329
    liste = []
    this_world_frame_offset = data[0x14461 + world] + frame
    offset_Y_1 = data[0x14461 + this_world_frame_offset]
    if offset_Y_1 != 0:
        offset_base = data[0x144D7 + offset_Y_1]
        current_offset = (offset_base & 0x00FF) + 0xC4D8
        count = data[0x8000 + current_offset]
        if count != 0:
            current_offset += 1
            for _ in range(count):
                door_data = data[0x8003 + current_offset]
                which_door = 0x1144 + int((door_data & 0x7F) / 2 / 2 / 2)
                bit_offset = door_data & 0x07
                bit_to_check = data[0x180B8 + bit_offset]
                something_0x22 = deepcopy(current_offset)  # Store Y for later?
                # Preparation just before calling the door remover
                map_tile = (data[0x8000 + current_offset],data[0x8000 + current_offset + 1])
                map_tile_offset = (0x8000 + current_offset,0x8000 + current_offset + 1)
                    # X screen coordinates to start the remover of tilemap and collision.

                # This has been done earlier in the code for some reason.
                something_OxA = data[0x8002 + current_offset]
                # print("0xA", hex(0x8002 + current_offset))

                # ne pas changer ce qui est en dessous jusqu'au append.
                # door_remover
                something_OxA //= 2

                size_to_remove = data[0x14452 + something_OxA]
                if size_to_remove == 68:
                    orientation = "N"
                elif size_to_remove == 66:
                    orientation = "S"
                elif size_to_remove == 36:
                    orientation = "EW"
                else:
                    raise BaseException(f"Something is wrong")



                # Tu peux changer l'ordre ou le contenu pour retirer hex et bin par exemple.
                liste.append((hex(which_door), bin(bit_to_check),map_tile_offset, orientation))
                    # which_door : (Présentement stringé, mais à déstringer). 
                    # bit_to_check : Présentement biné, c'est très visuel ainsi.
                        # which_door + bit_to_check : ces deux informations permettra de déterminer si deux portes vérifient la même condition
                            # Pour demeurer barré ou si elles se débarrent. Voir 0-5 et 0-8 pour un exemple.
                    # map_tile_offset : These two values are the offsets to experiment with in order to determine NSEW.
                    # orientation : Je ne pense pas que tu en aies besoin de ceci. Mais ça pourrait te servir pour valider tes
                        # affaires.
                current_offset += 4
    return liste



# 82C3BE : Door remover!!!!! Donc, de ce que j'en comprends, les portes sont préplacés, et on les enlèves à chaque fois.
    # Cette fonctione nlève aussi les portes de 1146. C'est donc une enleveuse de portes universelle.


def tester_all(data):
    worlds = [16,16,25,30,25]
    for world, nframes in enumerate(worlds):
        print(f"WORLD {world}-------------------------------------")
        for frame in range(nframes):
            if getters_doors(data, world, frame)!= []:
                print(getters_doors(data, world, frame))