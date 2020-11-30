

def getter_items(data, world):
    def boucle1(E,offset, liste=liste):
        def boucle2(offset, compte, liste=liste):
            """Boucle 2 is the loop that take care of the actual item retrieval.
            The code initially was a litteral translation of the assembly code.
            Then I modified the code to fit for the purposes of the randomizer. The codes
            not needed for the randomizer are commented.
            Among the lines of the code there are comment of codes that I wish to keep.


            """
            item_count = 0x0  # Reading a value in byte 0x0. Should be 0

            for _ in range(compte):
                info = data[offset] & 0xE0
                if info == 0:
                    # Pas de byte à gauche (Donc on a 0x00 à 0x0F)
                    X = item_count // 2
                    A = data[offset] & 0x0F
                    if item_count % 2 == 1:  # 80E54C
                        A = A  * 2 * 2 * 2 * 2  # 4x ASL
                    data[0x1160 + X] = data[0x1160 + X] | A
                    item_count += 1
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