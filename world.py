import random
from copy import deepcopy


def getter_exits(data, world_i, nFrames):
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

    exits_values = []
    exits_offsets = []
    exits_frames = []


    # Step 1 : Trouver la base.
    base = data[0x01F303 + world_i]

    all_frame_i = range(nFrames)  # Nombre random pour proof de concept. C'est le nombre de levels (frames) à aller chercher.
        # Si on veut un endroit précis précis (Exemple : 1-1), on doit éviter la boucle qui suit.
    for frame_i in all_frame_i:
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

class World():
    def __init__(self, data, world_i):
        assert isinstance(data, bytearray), "Must be a bytearray"
        assert 0 <= world_i <= 4, "Must be in range 0-4."

        all_nFrames = [16, 16, 26, 30, 26]
        all_bossFrame = [14, 15, 25, 25, 25]
        all_preBossFrame = [12, 14, 24, 24, 24]
        self.world_i = world_i
        self.data = data
        self.nFrames = all_nFrames[world_i]
        self.bossFrame = all_bossFrame[world_i]
        self.exits_offsets, self.exits_values, self.source_frames = getter_exits(data, world_i, self.nFrames)
        self.destination_frames = []
        self.destination_pos = []

        for this_exit_values in self.exits_values:
            self.destination_frames.append(this_exit_values[0])
            if this_exit_values[4]<25:
                self.destination_pos.append('W')
            elif this_exit_values[4]>230:
                self.destination_pos.append('E')
            elif this_exit_values[5]<40:
                self.destination_pos.append('N')
            elif this_exit_values[5]>190:
                self.destination_pos.append('S')
            else:
                self.destination_pos.append('?')

        for i,this_exit_values in enumerate(self.exits_values):
                if this_exit_values[0] == self.bossFrame:
                    self.preboss_index = i
                    break

        self.exit_pairs = []
        for i,source in enumerate(self.source_frames):
            for j,destination in enumerate(self.destination_frames):
                if (self.destination_frames[i] == self.source_frames[j])&(self.destination_frames[j] == self.source_frames[i]):
                    if sorted([i,j]) not in self.exit_pairs: 
                        self.exit_pairs.append(sorted([i,j]))

        self.nExits = len(self.source_frames)


    def randomize_exits(self, fix_boss_exit, keep_direction, pair_exits): #fix_boss_exit is a bool
        
        #determine new order
        if keep_direction & (not pair_exits):#keep direction
            new_order = list(range(self.nExits))
            for ref_destination_pos in ['N','S','W','E']:
                i_to_shuffle_now = [i for i, this_destination_pos in enumerate(self.destination_pos) if this_destination_pos == ref_destination_pos]
                if fix_boss_exit: 
                    if self.preboss_index in i_to_shuffle_now: i_to_shuffle_now.remove(self.preboss_index)
                shuffled_i = deepcopy(i_to_shuffle_now)
                random.shuffle(shuffled_i)
                for j,i in enumerate(i_to_shuffle_now):
                    new_order[i] = shuffled_i[j]

        elif (not keep_direction) & (pair_exits):#pair exits
            new_order = list(range(self.nExits))
            shuffled_pairs = deepcopy(self.exit_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(self.exit_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]

        elif keep_direction & pair_exits: #keep direction AND pair exits
            new_order = list(range(self.nExits))
            pairs_to_sort = deepcopy(self.exit_pairs)
            NS_pairs = []
            WE_pairs = []
            for pair in pairs_to_sort:
                if (self.destination_pos[pair[0]] == 'N') or (self.destination_pos[pair[0]] == 'S'):
                    NS_pairs.append(pair)
                elif (self.destination_pos[pair[0]] == 'W') or (self.destination_pos[pair[0]] == 'E'):
                    WE_pairs.append(pair)
            #North and South pairs
            shuffled_pairs = deepcopy(NS_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(NS_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]
            #West and East pairs
            shuffled_pairs = deepcopy(WE_pairs)
            random.shuffle(shuffled_pairs)
            for i,pair in enumerate(WE_pairs):
                new_order[pair[0]] = shuffled_pairs[i][0]
                new_order[shuffled_pairs[i][1]] = pair[1]

        else: #totally random
            new_order = list(range(self.nExits))
            random.shuffle(new_order)
            if fix_boss_exit:
                new_order.remove(self.preboss_index)
                new_order.insert(self.preboss_index,self.preboss_index)
            

        #assign elements in new order
        old_exits_values = deepcopy(self.exits_values)
        for i,temp in enumerate(old_exits_values):
            self.exits_values[i][0] = old_exits_values[new_order[i]][0]
            self.exits_values[i][4] = old_exits_values[new_order[i]][4]
            self.exits_values[i][5] = old_exits_values[new_order[i]][5]

        return self.exits_values
