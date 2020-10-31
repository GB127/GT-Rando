from gameclass import GT


def getter(data, world):
    """Fonction allant chercher les éléments nécessaires.
        Big thank you to Psychomaniac, reference : https://pastebin.com/y8yYPcfd

        Voici la logique :
            1- Lecture d'un byte à un endroit précis qui dépend du World. L'info sera un premier offset. C'est la base.
                offset 1 = 0x01F303 + World  ou $83:F303 + level_index
            2- L'endroit de lecture suivant dépend du level et de la lecture précédente. Ça donne un autre offset.
                NOTE : ON DOIT LIRE UN "BIG BYTE", DONC ON LIT LE BYTE SUIVANT POUR LE HIGH ENDIAN chose.
                offset 2 = 0x1F303 + offset 1 + 2 * level
            3- La lecture à ce dernier offset donnera de sinfos sur la quantité de exits à loader et leur endroit.
                0x10000 + offset2
            4- On load les informations des exits qui sont entreposés dans les cinq offsets suivants.

        Args:            data (bytearray): data du jeu.
            World (int): World que l'on veut loader.


        Return : Liste de liste qui contient les 6 infos des exits.
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
    # J'ai fait ces deux checks juste pour le fun et au cas où...
    assert isinstance(data, bytearray), "Must be a bytearray"
    assert 0 <= world <= 4, "Must be in range 0-4."  # Failcheck already. Not sure if useful.

    # Step 1 : Trouver la base.
    base = data[0x01F303 + world]
    liste = []

    j = range(8)  # Nombre random pour proof de concept. C'est le nombre de levels (frames) à aller chercher.
    for number in j:
        # On doit trouver l'endroit du count.

        # On doit aller chercher le GROS byte. et pour cela, on doit avoir un "adjust" qui est dépendant du frame.
        adjust = 0x1F303 + base + 2*number

        #Lecture du Gros Byte. On doit lire le byte présent et le byte suivant et les combiner ensemble.
            # GROS BYTE : 0xHHpp
        test3 = data[0x1F303 + base + 2*number]  # Cecu est l'endroit où es tle count, du moins les deux premiers bytes on a les deux premiers chiffres! (pp)
        test4 = data[0x1F303 + base + 2*number + 1]  # Les deux high bytes (HH)

        # Donc le fond on doit faire 2 shift left pour ajouter deux zeros. 
        # Puis additionner.
            # 0xHH => 0xHH00 => 0xHHpp

        # Je ne comprends pas pourquoi 16^2 ne fonctionne psa ici.

        test5 = test4 * 16 * 16 + test3  

        # Trouvons enfin l'endroit du count.
        test6 = 0x10000 + test5
        count = data[test6]  # This will be the count.

        for i in range(count):
            liste.append([data[test6 + x + 6 * i + 1] for x in range(6)])
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

    return liste  # On retourne la liste


with open("Vanilla.smc", "rb") as original:
    originaldata = original.read()
    randogame = GT(originaldata)
    print(getter(randogame.data, 3))
