
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



def getter_exits(data, world_i, Frames=[]):
    """Fonction allant chercher les offsets ET les valeurs. Je ne sais pas encore si on a besoin 
        des deux ou pas. Donc j'ai retourné les deux.

        Big thank you to Psychomaniac, reference : https://pastebin.com/y8yYPcfd

        Voici la logique :
            1- Lecture d'un byte à un endroit précis qui dépend du World. L'info sera un premier offset. C'est la base.
                offset 1 = 0x01F303 + World  ou $83:F303 + level_index
            2- L'endroit de lecture suivant dépend du level et de la lecture précédente. Ça donne un autre offset.
                NOTE : ON DOIT LIRE UN "BIG BYTE", DONC ON LIT LE BYTE SUIVANT POUR LE HIGH ENDIAN chose.
                offset 2 = 0x1F303 + offset 1 + 2 * level
            3- La lecture à ce dernier offset donnera l'infos sur la quantité de exits à loader.
                0x10000 + offset2
            4- On load les informations des exits qui sont entreposés dans les cinq offsets par exits.
                Le premier débute au offset juste après la lecture à l'étape 3.

        Args:
            data (bytearray): data du jeu.
            World (int): World que l'on veut loader.


        Return (tuple): exits_offsets, exits_values
            exits_offsets (liste): Liste de liste qui contient les 6 offsets des exits.
            exits_values (liste): Liste de liste qui contient les 6 infos des exits.
                [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5] ...]
                0 : Screen this exit leads to
                1 : Base tile index on collision map
                2 : Pas spécifié par psychomaniac
                3 : Type d'exit, It specifies how the exit's collision tiles are laid down, See below.
                    If bit 6 is set (0x20) then it is a vertical line, otherwise it is horizontal or 2x2
                    If bit 6 is not set and bits 1-4 are 0x0F, then the exit is 2x2 (x,y) (x+1,y) (x,y+1) and (x+1,y+1)
                    For horizontal or vertical lines, bits 1-4 specify the length and bit 5 says if it is 1 or 2 tiles thick.
                4 : X position on the destination screen to place Max and/or Goofy
                5 : Y position on the destination screen to place Max and/or Goofy

        """
    # J'ai fait ces deux checks au cas où.
    assert isinstance(data, bytearray), "Must be a bytearray"
    assert 0 <= world_i <= 4, "Must be in range 0-4."
    assert Frames is not iter(Frames), "Must be an iterable"

    exits_values = []
    exits_offsets = []
    exits_frames = []


    # Step 1 : Trouver la base.
    base = data[0x01F303 + world_i]
    for frame_i in Frames:
    # J'ai mis ces lignes en commentaires, car ces lignes forcent l'itération. 
    # Je pense que l'itération serait beaucoup mieux
    # Si elle était faite en dehors de la fonction.

    # Comme ça, ça nous permet d'aller chercher spécifiquement les exits à UN endroit souhaité.

            # On doit trouver l'endroit du count.

            # On doit aller chercher le GROS byte. et pour cela, on doit avoir un "adjust" qui est dépendant du frame.
        adjust = 0x1F303 + base + 2*frame_i

        #Lecture du Gros Byte. On doit lire le byte présent et le byte suivant et les combiner ensemble.
            # GROS BYTE : 0xHHpp
        temp1 = data[0x1F303 + base + 2*frame_i]  # Cecu est l'endroit où es tle count, du moins les deux premiers bytes on a les deux premiers chiffres! (pp)
        temp2 = data[0x1F303 + base + 2*frame_i + 1]  # Les deux high bytes (HH)

        # Donc le fond on doit faire 2 shift left pour ajouter deux zeros. 
        # Puis additionner.
            # 0xHH => 0xHH00 => 0xHHpp
        # Je ne comprends pas pourquoi 16^2 ne fonctionne psa ici.

        temp3 = temp2 * 16 * 16 + temp1  

        # Trouvons enfin l'endroit du count.
        temp4 = 0x10000 + temp3
        count = data[temp4]  # This will be the count.

        for i in range(count):
            exits_offsets.append(list(temp4 + x + 6 * i + 1 for x in range(6)))  # Voici les offsets.
            # Il devrait être possible d'utiliser Exit() ici.
            exits_values.append([data[temp4 + x + 6 * i + 1] for x in range(6)])  # Voici les valeurs retrouvées dans chaque offsets.
            exits_frames.append(frame_i)
            """
                0 : Screen this exit leads to
                1 : Base tile index on collision map
                2 : Pas spécifié par psychomaniac
                3 : Type d'exit, It specifies how the exit's collision tiles are laid down, See below.
                    If bit 6 is set (0x20) then it is a vertical line, otherwise it is horizontal or 2x2
                    If bit 6 is not set and bits 1-4 are 0x0F, then the exit is 2x2 (x,y) (x+1,y) (x,y+1) and (x+1,y+1)
                    For horizontal or vertical lines, bits 1-4 specify the length and bit 5 says if it is 1 or 2 tiles thick.
                4 : X position on the destination screen to place Max and/or Goofy
                5 : Y position on the destination screen to place Max and/or Goofy
            """
    return exits_offsets, exits_values, exits_frames  # On retourne les listes

def getter_passwords(world):
    """Return the offsets of all passwords
        Args:
            world (int or str):
                int : World you want to get.
                str : "all" if all offset is desired.

        Returns:
            list : offsets of the said world.
    """
    if world == "all":
        return list(range(0x1C67F, 0x1C693))
    return [x for x in range(0x1C67F + 5*(world -1), 0x1C684 + 5*(world-1))]
