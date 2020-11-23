from copy import deepcopy

def getters_doors(data, world, frame):  #82C329
    # Structure par exits:
    # 0 : Où sur l'écran
    # 1 : Où sur l'écran (High byte)
    # 2 : Forme de la porte (Pour pouvoir bien l'éffacer)
    # 3 : format de la porte
        # Pour le retour, ici je l'ai décomposée en deux
            # Which door
            # Bit to check

    liste = []
    offset_Y_1 = data[0x14461 + data[0x14461 + world] + frame]
    if offset_Y_1 != 0:
        current_offset = (data[0x144D7 + offset_Y_1] & 0x00FF) + 0xC4D8
        count = data[0x8000 + current_offset]
        if count != 0:
            current_offset += 1
            for _ in range(count):
                base_door = 0x8000 + current_offset
                map_tile_offset = (base_door,
                                   base_door + 1)  # 0 et 1 ensemble. À séparer si tu préfères.
                forme = data[base_door + 2]
                door_data = data[base_door + 3]

                # Manipulations à faire pour récupérer la bonne information pour la logique. Je décortiquerai sous peu.
                which_door = 0x1144 + int((door_data & 0x7F) / 2 / 2 / 2)
                bit_offset = door_data & 0x07
                bit_to_check = data[0x180B8 + bit_offset]


                # ne pas changer ce qui est en dessous jusqu'au append.
                # door_remover
                forme //= 2

                size_to_remove = data[0x14452 + forme]
                if size_to_remove == 68:
                    orientation = "N"
                elif size_to_remove == 66:
                    orientation = "S"
                elif size_to_remove == 36:
                    orientation = "EW"
                else:
                    raise BaseException(f"Something is wrong")

                # Tu peux changer l'ordre ou le contenu pour retirer hex et bin par exemple. Présentement ça suit le plus fidèlement
                # possible l'ordre dans le data.
                liste.append([map_tile_offset, forme, hex(which_door), bin(bit_to_check), orientation])
                    # which_door : (Présentement stringé, mais à déstringer). 
                    # bit_to_check : Présentement biné, c'est très visuel ainsi.
                        # which_door + bit_to_check : ces deux informations permettra de déterminer si deux portes vérifient la même condition
                            # Pour demeurer barré ou si elles se débarrent. Voir 0-5 et 0-8 pour un exemple.
                    # map_tile_offset : These two values are the offsets to experiment with in order to determine NSEW.
                    # orientation : Je ne pense pas que tu en aies besoin de ceci. Mais ça pourrait te servir pour valider tes
                        # affaires?
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