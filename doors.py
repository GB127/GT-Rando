from copy import deepcopy
def door_adder(data,
                  world, frame,
                  tile_high, tile_low,
                  forme,
                  which_door):  #82C329
    # WARNING : Je dois faire des modifications dans le jeu pour nous permettre une plus grand flexibilité
    # dans l'emplacement des portes. Mais le code en soit est fonctionnel.

    # Comme door remover : Incomplet, car n'enlève pas le tile map. 
    # Mais le adder détruit le jeu en quelque sorte. À ne pas utiliser pour l'instant, sauf pour tester
    # seulement si une exit vanilla (préexistante) existait préalablement.

    # Forme : Forme de l'efface. Argument Possiblement enlèvable avec tile_high et tile_low.
        # 0, 4 ou 2
            # 0 = N
            # 4 = S
            # 2 = EW
    # Which door : 0-32

    offset_Y_1 = data[0x14461 + data[0x14461 + world] + frame]
    if offset_Y_1 != 0:
        current_offset = (data[0x144D7 + offset_Y_1] & 0x00FF) + 0xC4D8
        vanilla_count = deepcopy(data[0x8000 + current_offset])
        data[0x8000 + current_offset] += 1
        current_offset += 1
        if vanilla_count != 0:
            for _ in range(vanilla_count): current_offset += 4
        base_door = 0x8000 + current_offset

        data[base_door] = tile_low
        data[base_door + 1] = tile_high
        data[base_door + 2] = forme

        # manips pour convertir which_door:
        bits_3_6 = (which_door // 8)  * 2 * 2 * 2
        bits_0_2 = which_door % 8
        data[base_door + 3] = bits_0_2 + bits_3_6
        # J'ose croire que bit # 7 c'est pour la clé du boss. À vérifier.

def getters_doors(data, world, frame):  #82C329
    # Structure par exits:
    # 0 : Où sur l'écran
    # 1 : Où sur l'écran (High byte)
    # 2 : Forme de la porte (Pour pouvoir bien l'éffacer)
    # 3 : format de la porte
        # Bit 0-2 :

        # Bit 3-6 : 0x1144, 0x1145, 0x1146 ou 0x1147.
            # Sera tjs 0x1144 ou 0x1145 dans vanilla.


        # Pour le retour, ici je l'ai décomposée en deux
            # Which door
            # Bit to check
        # Ceci peut être modifié pour être en une seule liste pour savoir 
        # quelle condition est vérifiée. Maintenant que je sais que mes trois fonctions
        # foncitonnent parfaitement, je ferai cette modification pour simplifier le check de la logique
        # bientôt.

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
                    # C'est avec ce deux infos si-dessuss que l'on va pouvoir déterminer si C'est une porte
                    # N,S,E ou W.
                forme = data[base_door + 2]
                door_data = data[base_door + 3]

                # Manipulations à faire pour récupérer la bonne information pour la logique.
                which_door = 0x1144 + int((door_data & 0x7F) / 2 / 2 / 2)
                bit_offset = door_data & 0x07
                bit_to_check = data[0x180B8 + bit_offset]

                # Je suis convaincu que ce qui suit ci-dessous peut être enlevé. Mais je l'ai
                # laissé au cas où pour te permettre de te vérifier après ton gossage de debug.py.
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

                    # Va être BIENTÔT CHANGÉ POUR simplifie rla vie.
                        # which_door : (Présentement stringé)
                        # bit_to_check : Présentement biné, c'est très visuel ainsi. À débiné lorsque compris. Ces infos sont contenues dans 3 sous une certaine forme...
                            # which_door + bit_to_check : ces deux informations permettra de déterminer si deux portes vérifient la même condition.
                                # Pour demeurer barré ou si elles se débarrent. Voir 0-5 et 0-8 pour un exemple. Important pour la logique.
                        # Le changement proposé : une liste de 32 éléments (32, car le jeu offre cette possibilité, reste à vérifier si on peut avoir 32 clés en tout).

                    # map_tile_offset : These two values are the offsets to experiment with in order to determine NSEW.

                    # À ENLEVER PROBABLEMENT
                    # orientation : Je ne pense pas que tu en aies besoin de ceci. Mais ça pourrait te servir pour valider tes
                        # affaires?
                current_offset += 4
    return liste



def tester_all(data):
    # Fonction testeuse qui va aller printer tous les getters possibles.
    # Print seulement s'il y a une porte.
    worlds = [16,16,25,30,25]
    for world, nframes in enumerate(worlds):
        print(f"WORLD {world}-------------------------------------")
        for frame in range(nframes):
            if getters_doors(data, world, frame)!= []:
                print(getters_doors(data, world, frame))

def door_remover(data, world, frame, index):  #82C329
    # Incomplet en quelque sorte vu que ça n'enlève pas le tilemap et toute.
    # Mais ceci désactive la porte. Même si la porte est là, elle n'est pas là!

    offsets, values = [], []

    offset_Y_1 = data[0x14461 + data[0x14461 + world] + frame]
    if offset_Y_1 != 0:
        current_offset = (data[0x144D7 + offset_Y_1] & 0x00FF) + 0xC4D8
        vanilla_count = deepcopy(data[0x8000 + current_offset])
        data[0x8000 + current_offset] -= 1
        if vanilla_count != 0:  # Data collecting
            current_offset += 1
            for _ in range(vanilla_count):
                tempo, tempo_v = [], []
                # Tilemap locaton [0-1]
                tempo.append(0x8000 + current_offset)
                tempo.append(0x8000 + current_offset + 1)
                tempo_v.append(data[0x8000 + current_offset])
                tempo_v.append(data[0x8000 + current_offset + 1])

                # Forme related [2]
                tempo.append(0x8002 + current_offset)
                tempo_v.append(data[0x8002 + current_offset])
                forme = data[0x8002 + current_offset]
                forme //= 2
                tempo.append(0x14452 + forme)  # Tilemap format to remove.
                tempo_v.append(data[0x14452 + forme])


                # Format de la porte [3] et ses caractéristiques
                tempo.append(0x8003 + current_offset)
                tempo_v.append(data[0x8003 + current_offset])

                door_data = data[0x8003 + current_offset]
                bit_offset = door_data & 0x07

                tempo.append(0x180B8 + bit_offset)
                tempo_v.append(data[0x180B8 + bit_offset])

                bit_to_check = data[0x180B8 + bit_offset]

                offsets.append(tempo)
                values.append(tempo_v)
                current_offset += 4

    # Décalage des valeurs au cas où un frame aurait plus qu'une porte barrée.
        # N'arrivera jamais en vanilla. Mais possiblement au rando et donc on couvre
        # cette possibilité avec ceci!

    for kit_offset in offsets[index:]:
        tempo = []
        current_index = offsets.index(kit_offset)
        try:
            for no, offset in enumerate(kit_offset):
                data[offset] = values[current_index+1][no]
                tempo.append(data[offset])
        except IndexError:
            pass
