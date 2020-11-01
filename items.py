from gameclass import GT

def getter_items(data, world):
    liste = []
    def boucle1(E,offset, liste=liste):
        def boucle2(offset, compte, liste=liste):
            item_count = 0x0  # Reading a value in byte 0x0. Should be 0 

            for _ in range(compte):
                info = data[offset] & 0xE0  # Ceci est pour vérifier si On a un byte à gauche
                if info == 0:
                    # Pas de byte à gauche (Donc on a 0x00 à 0x0F)
                    
                    liste.append(offset)  # Cette ligne est la seule différence avec le code d'assembleur! Tout le reste est une traduction littérale.
                    
                    # Cette section ne sert à rien pour le randomizer. Mais je le conserve, car c'est la traduction pythonique du code intégral.
                    """
                    X = item_count // 2
                    A = data[offset] & 0x0F  # On vérifie si byte de droite est présent
                    if item_count % 2 == 1:  # 80E54C
                        A = A  * 2 * 2 * 2 * 2  # 4x ASL, je ne sais pas comment faire mieux que ça ahah.
                    data[0x1160 + X] = data[0x1160 + X] | A
                    item_count += 1
                    """
                offset += 4  # E55A
            return offset
        ####################################
        for _ in range(E):
            compte = data[offset]
            offset += 1
            if compte == 0:
                pass
            if compte != 0:
                    offset = boucle2(offset, compte)
    ########################################
    offset1 = data[0x6E6A + world]

    E = data[0x66D6 + world] # I don't understand what this value means specifically.

    item_offset1 = data[0x6E6A + offset1 + 1]
    item_offset2 = data[0x6E6A + offset1]

    item_offset = item_offset1 * 16 * 16 + item_offset2 - 0x8000  # Ça fonctionne...

    boucle1(E, item_offset)

    return liste