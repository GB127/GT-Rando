from gameclass import GT

def getter_items(data, world):
    liste = []
    def boucle1(E,offset, liste=liste):
        def boucle2(offset, compte, liste=liste):
            item_count = data[0x0]

            for _ in range(compte):
                info = data[offset] & 0xE0  # Ceci est pour vérifier si On a un byte à gauche
                if info == 0:  # 80E541
                    # Pas de byte à gauche (Donc on a 0x00 à 0x0F)
                    X = item_count // 2
                    liste.append(offset)
                    A = data[offset] & 0x0F  # On vérifie si byte de droite est présent
                    if item_count % 2 == 1:  # 80E54C
                        A = A  * 2 * 2 * 2 * 2  # 4x ASL, je ne sais pas comment faire mieux que ça ahah.
                    item_count += 1
                    data[0x1160 + X] = data[0x1160 + X] | A
                offset += 4  # E55A
            return offset
        ####################################
        for _ in range(E):  # La boucle semble fonctionner
            compte = data[offset]
            offset += 1  # Ça fonctionne
            if compte == 0:
                pass
            if compte != 0:
                    offset = boucle2(offset, compte)
    ########################################
    offset1 = data[0x6E6A + world]  # Ceci fonctionne

    E = data[0x66D6 + world]  # Ceci devrait fonctionner.

    item_offset1 = data[0x6E6A + offset1 + 1]
    item_offset2 = data[0x6E6A + offset1]

    item_offset = item_offset1 * 16 * 16 + item_offset2 - 0x8000  # Ça fonctionne... 

    boucle1(E, item_offset)

    return liste