def indices(data,world, frame):
    World = world
    Map = frame
    toreturn = []

    offset1 = 2* Map + data[World + 0x6E6A]

    offset2 = data[offset1 + 0x6E6A]
    offset3 = data[offset1 + 0x6E6A + 1]

    offset4 = offset3 * 16 * 16 + offset2 - 0x8000

    count = data[offset4]
    if count != 0:
        offset4 += 1
        for _ in range(count):
            X = data[offset4]
            X = X & 0xE0
            X = X // 16
            if X == 0x0:
                # There is something with 0x0 à regarder.
                something4 = data[offset4 + 1]
                offset5 = something4 // 2  # C'EST CE QUE JE CHERCHE
                carry = something4 % 2
                toreturn.append((offset5, carry))
            offset4 += 4
    return toreturn

def getter_items(data, world):
    """Retrieve the offsets of all the items in a given world.
        NOTES:
            The code initially was a litteral translation of the assembly code.
            Then I removed some codes to fit for the purposes of the randomizer. The codes
            not needed for the randomizer are removed. The original translation is still available.

        Args:
            data ([bytearray]): the game data.
            world ([int]): The world you want the infos.
        
        Return list of offsets
        """

    liste = []
    def boucle1(E,offset, liste=liste):
        """I am honestly not sure to understand why the entire code is like that.
            """
        def boucle2(offset, compte, liste=liste):
            """Boucle 2 is the loop that take care of the actual item retrieval.
                This boucle checks for if an item is to be stored.
            """
            for _ in range(compte):
                info = data[offset] & 0xE0
                if info == 0:
                    # Pas de byte à gauche (Donc on a 0x00 à 0x0F)
                    liste.append(offset)
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
