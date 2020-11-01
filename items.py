from gameclass import GT

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