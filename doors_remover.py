from copy import deepcopy

def door_remover(data, world, frame, index):  #82C329
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
