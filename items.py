from getters import getter_items, getter_items_indices
class Items:
    def __init__(self, data, world_i):
        
        all_nFrames = [16, 16, 26, 30, 26]
        self.nFrames = all_nFrames[world_i]
        # getter utilization
        self.offsets,self.values,self.frames = self.getWorldItemsFromData(data,world_i)

    def getWorldItemsFromData(self, data, world_i):
        for frame_i in range(self.nFrames):
            print(self.getFrameItemsFromData(data, world_i, frame_i))

    def getFrameItemsFromData(self, data, world_i, frame_i):
        result = []
        offset1 = 2* frame_i + data[world_i + 0x6E6A]

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
                    offset5 = data[offset4 + 1] // 2
                    carry = data[offset4 + 1] % 2
                    result.append((offset5, carry))
                offset4 += 4
        if result != []:
            return result
        else:
            return []

def getter_items_indices(data, world, frame):
    """Getter for getting the correct indices for each items that has an item.
        return None if no items on the frame.

        Args:
            data (bytearray): game data.
            world (int): World, ranging from 0 to 4.
            frame (int): frame you want to fetch.

        Returns if items:
            list of tuples : (indices, GvsD)
                GvsD = Will determine if Left or right of the 0xXX.
                In pythonic code, we could can do 2* indices + Gvs.D
    """
    toreturn = []

    offset1 = 2* frame + data[world + 0x6E6A]

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
                something4 = data[offset4 + 1]
                offset5 = something4 // 2
                carry = something4 % 2
                toreturn.append((offset5, carry))
            offset4 += 4
    if toreturn != []:
        return toreturn
    else:
        return None

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

